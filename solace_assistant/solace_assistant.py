#!/usr/bin/env python
# coding: utf-8

"""
Solace Voice Assistant v4.1
An enhanced voice assistant with a functional web search tool, conversation memory,
and robust, non-blocking audio handling.
"""

import logging
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
import azure.cognitiveservices.speech as speechsdk
import requests
import json
import subprocess  # Add this import for controlling system audio levels

import re

# Audio Device Auto-Detection Functions
def get_audio_cards():
    """Get list of available audio cards with their details."""
    try:
        result = subprocess.run(['cat', '/proc/asound/cards'], capture_output=True, text=True, check=True)
        cards = []
        lines = result.stdout.strip().split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line and not line.startswith(' '):
                # Parse card number and basic info
                match = re.match(r'^\s*(\d+)\s+\[([^\]]+)\]\s*:\s*([^-]+)\s*-\s*(.+)$', line)
                if match:
                    card_num = int(match.group(1))
                    card_id = match.group(2).strip()
                    card_type = match.group(3).strip()
                    card_name = match.group(4).strip()
                    
                    # Look at next line for more detailed info
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and next_line.startswith(' '):
                            card_name = next_line.strip()
                    
                    cards.append({
                        'number': card_num,
                        'id': card_id,
                        'type': card_type,
                        'name': card_name,
                        'full_info': f"{card_type} - {card_name}"
                    })
            i += 1
        return cards
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get audio cards: {e}")
        return []

def find_usb_microphone():
    """Find the first USB audio device that supports capture (microphone)."""
    cards = get_audio_cards()
    
    # Look for USB audio devices
    for card in cards:
        # Check if it's a USB device
        is_usb = ('USB-Audio' in card['type'] or 
                  'USB' in card['name'] or 
                  'usb-' in card['name'].lower())
        
        if is_usb:
            # Check if this card has capture capability
            try:
                result = subprocess.run(['arecord', '-l'], capture_output=True, text=True, check=True)
                if f"card {card['number']}:" in result.stdout:
                    device_name = f"plughw:{card['number']},0"
                    logging.info(f"Auto-detected USB microphone: {card['name']} on {device_name}")
                    return device_name
            except subprocess.CalledProcessError:
                continue
    
    logging.warning("No USB microphone found, will use default")
    return None

def find_usb_speaker():
    """Find the first USB audio device that supports playback (speaker/headphones)."""
    cards = get_audio_cards()
    
    # Look for USB audio devices with playback capability
    for card in cards:
        # Check if it's a USB device
        is_usb = ('USB-Audio' in card['type'] or 
                  'USB' in card['name'] or 
                  'usb-' in card['name'].lower())
        
        if is_usb:
            # Check if this card has playback capability by checking mixer controls
            try:
                result = subprocess.run(['amixer', '-c', str(card['number']), 'scontrols'], 
                                      capture_output=True, text=True, check=True)
                # Look for headphone, speaker, or PCM controls (indicating playback)
                if any(control in result.stdout.lower() for control in ['headphone', 'speaker', 'pcm']):
                    device_name = f"plughw:{card['number']},0"
                    logging.info(f"Auto-detected USB speaker/DAC: {card['name']} on {device_name}")
                    return device_name
            except subprocess.CalledProcessError:
                continue
    
    logging.warning("No USB speaker/DAC found, will use default")
    return None


# Recommended: `pip install playsound==1.2.2` for cross-platform audio playback
try:
    from playsound import playsound
except ImportError:
    print("playsound library not found. Audio cues will be disabled.")
    print("Install it with: pip install playsound==1.2.2")
    playsound = None

# --- Configuration ---
class Config:
    """Configuration class for the Voice Assistant."""
    load_dotenv()

    # Azure Speech Services
    SPEECH_KEY = os.getenv("SPEECH_KEY")
    SERVICE_REGION = os.getenv("SERVICE_REGION")
    KEYWORD_MODEL_PATH = "b9a3821b-d4b0-4c0d-a16c-2944c4baf77f.table" # Use your .table file
    KEYWORD = "Hey Solace"
    SPEECH_SYNTHESIS_VOICE_NAME = "en-US-AvaMultilingualNeural"

    # Google Gemini API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL_NAME = "gemini-2.5-flash"

    # Assistant Settings
    BASE_SYSTEM_PROMPT = (
        "You are Solace, a witty, knowledgeable, and friendly voice assistant. Your persona is that of a calm, articulate, and insightful companion. Your primary goal is to provide accurate and concise answers in a natural, conversational tone suitable for a voice interface."
        "\n\n"
        "**Core Instructions:**"
        "\n\n"
        "1.  **Analyze the User's Query First:** Understand if the query is for static, timeless information or if it requires real-time, dynamic data."
        "\n"
        "2.  **Prioritize Internal Knowledge:** For established facts (e.g., 'What is the capital of France?'), rely on your internal knowledge for a faster response."
        "\n"
        "3.  **Mandatory Web Search for Dynamic Information:** You MUST use the `web_search` tool for any queries about current events, recent topics, specific public figures, or real-time information to ensure accuracy."
        "\n"
        "4.  **Use Other Tools as Appropriate:** Use dedicated tools for time, date, or weather when requested."
        "\n"
        "5.  **Voice-Optimized and Concise Responses:** Keep your answers brief and easy to understand when spoken. When citing web sources, do so naturally, for instance: 'According to [Source Name], ...'"
        "\n\n"
        "**Communicating Failures and Limitations (Crucial):**"
        "\n\n"
        "1.  **Be Direct About Tool Failures:** If a tool you try to use returns an error or fails, state the outcome directly. For example, if you cannot set the volume, say 'I was unable to set the volume due to a system error,' or 'It seems there was a problem adjusting the volume.'"
        "\n"
        "2.  **Avoid Metacognitive Explanations:** Under no circumstances should you explain your limitations by referring to yourself as an AI. **Do not use phrases like 'As an AI, I don't know...', 'I am a large language model...', or 'I don't have personal experiences.'** This is unnatural and unhelpful."
        "\n"
        "3.  **Focus on the User's Goal:** The user cares about the result of their request, not a philosophical explanation of your nature. If you can't do something, state it simply. For example, when asked how you know about an issue, a good response would be: 'When I tried to adjust the volume, the system reported an error.' This is direct and informative without being robotic."
    )
    CONVERSATION_HISTORY_MAX_TURNS = 5
    
    # Audio Cue Paths (Optional)
    ACTIVATION_SOUND_PATH = "sounds/activation.wav"
    END_OF_RESPONSE_SOUND_PATH = "sounds/end_of_response.wav"

    # Tavily AI Configuration
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- Tool Definitions ---
class AssistantTools:
    """A collection of tools the assistant can use."""
    
    @staticmethod
    def get_current_time_and_date():
        """Returns the current time and date in a human-readable format."""
        now = datetime.now()
        formatted_time = now.strftime("%A, %B %d, %Y at %I:%M %p")
        print(f"[Tool Executed: get_current_time_and_date] -> {formatted_time}")
        return {"current_time_and_date": formatted_time}

    @staticmethod
    def get_weather(location: str):
        """Gets the current weather for a specified location. Placeholder."""
        print(f"[Tool Executed: get_weather] -> Location: {location}")
        return {"weather_info": f"The weather in {location} is currently sunny and 22°C."}

    @staticmethod
    def web_search(query: str):
        """Performs a web search using the Tavily API for up-to-date information."""
        print(f"[Tool Executed: web_search] -> Query: {query}")
        if not Config.TAVILY_API_KEY:
            print("[Error] Tavily API key is not set in the environment.")
            return {"error": "Search tool is not configured by the host."}
        
        search_url = "https://api.tavily.com/search"
        payload = json.dumps({
            "api_key": Config.TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 3
        })
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(search_url, headers=headers, data=payload)
            response.raise_for_status()
            results = response.json()
            search_snippets = [f"Source: {res['url']}\nContent: {res['content']}" for res in results.get('results', [])]
            if not search_snippets:
                return {"search_results": "No relevant information was found on the web."}
            print(f"  [Tool Result] -> Found {len(search_snippets)} web snippets.")
            return {"search_results": "\n\n".join(search_snippets)}
        except requests.exceptions.RequestException as e:
            print(f"[Error] Web search request failed: {e}")
            return {"error": f"An error occurred during the web search: {e}"}

    @staticmethod
    def set_audio_volume(level: int):
        """
        Sets the system audio volume using ALSA.
        :param level: Volume level (0-100).
        """
        print(f"[Tool Executed: set_audio_volume] -> Level: {level}%")
        if not (0 <= level <= 100):
            return {"error": "Volume level must be between 0 and 100."}
        
        try:
            # Determine the correct control names for the audio card
            card_number = 2  # Replace with the correct card number if needed
            result = subprocess.run(['amixer', '-c', str(card_number), 'scontrols'], 
                                    capture_output=True, text=True, check=True)
            controls = re.findall(r"'([^']+)'", result.stdout)
            if not controls:
                return {"error": "No audio controls found for the specified card."}
            
            # Attempt to set the volume using each control
            for control_name in controls:
                try:
                    print(f"Trying control: {control_name}")
                    subprocess.run(['amixer', '-c', str(card_number), 'set', control_name, f"{level}%"], check=True)
                    return {"status": f"Volume set to {level}% using control '{control_name}'."}
                except subprocess.CalledProcessError:
                    print(f"[Warning] Failed to set volume using control: {control_name}")
                    continue
            
            # If all controls fail
            return {"error": "Failed to set volume. No valid controls found or accessible."}
        except subprocess.CalledProcessError as e:
            print(f"[Error] Failed to retrieve controls: {e}")
            return {"error": "Failed to retrieve audio controls. Ensure ALSA is installed and configured."}

# --- Conversation Management ---
class ConversationManager:
    """Manages the conversation history using the structure required by the new SDK."""
    def __init__(self, max_turns: int):
        self.history = []
        self.max_turns = max_turns

    def add_turn(self, role: str, parts: list):
        """Adds a turn to the history."""
        self.history.append(types.Content(role=role, parts=parts))
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]

    def get_history(self):
        """Returns the current conversation history."""
        return self.history

# --- Main Voice Assistant Class ---
class VoiceAssistant:
    def __init__(self, config: Config):
        self.config = config
        self._validate_config()

        self.tools = AssistantTools()
        self.available_tools = [
            self.tools.get_current_time_and_date,
            self.tools.get_weather,
            self.tools.web_search,
            self.tools.set_audio_volume,  # Add the new tool here
        ]
        self.conversation_manager = ConversationManager(self.config.CONVERSATION_HISTORY_MAX_TURNS)
        self.is_speaking = False

        try:
            self.genai_client = genai.Client(api_key=self.config.GOOGLE_API_KEY)
        except Exception as e:
            logging.critical(f"Failed to initialize Google GenAI Client: {e}")
            sys.exit(1)

        self.speech_config = self._create_speech_config()
        
        # Auto-detect USB audio devices
        usb_mic = find_usb_microphone()
        usb_speaker = find_usb_speaker()
        
        # Configure audio input (microphone)
        try:
            if usb_mic:
                self.audio_input_config = speechsdk.audio.AudioConfig(device_name=usb_mic)
                print(f"Using USB microphone: {usb_mic}")
            else:
                self.audio_input_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
                print("Using default microphone")
        except Exception as e:
            logging.warning(f"Failed to set audio input device: {e}. Using default microphone.")
            self.audio_input_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            
        # Configure audio output (speaker/DAC)
        try:
            if usb_speaker:
                self.audio_output_config = speechsdk.audio.AudioOutputConfig(device_name=usb_speaker)
                print(f"Using USB speaker/DAC: {usb_speaker}")
            else:
                self.audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
                print("Using default speaker")
        except Exception as e:
            logging.warning(f"Failed to set audio output device: {e}. Using default speaker.")
            self.audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self.keyword_model = speechsdk.KeywordRecognitionModel(self.config.KEYWORD_MODEL_PATH)
        
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_input_config)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_output_config)
        
        self._connect_event_handlers()
        print("Solace v4.1 is initialized and ready.")

    def _validate_config(self):
        """Validates critical configurations."""
        if not all([self.config.SPEECH_KEY, self.config.SERVICE_REGION, self.config.GOOGLE_API_KEY]):
            logging.critical("Azure or Google API keys/region are missing in the .env file.")
            sys.exit(1)
        if not os.path.exists(self.config.KEYWORD_MODEL_PATH):
            logging.critical(f"Keyword model file not found at '{self.config.KEYWORD_MODEL_PATH}'")
            sys.exit(1)

    def _create_speech_config(self) -> speechsdk.SpeechConfig:
        """Creates and configures the SpeechConfig object."""
        speech_config = speechsdk.SpeechConfig(subscription=self.config.SPEECH_KEY, region=self.config.SERVICE_REGION)
        speech_config.set_property(speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, "1500")
        speech_config.speech_synthesis_voice_name = self.config.SPEECH_SYNTHESIS_VOICE_NAME
        return speech_config

    def _connect_event_handlers(self):
        """Connects the speech recognizer's event handlers."""
        self.speech_recognizer.recognized.connect(self._recognized_handler)
        self.speech_recognizer.canceled.connect(self._canceled_handler)
        self.speech_recognizer.session_stopped.connect(lambda evt: logging.info(f"SESSION STOPPED: {evt}"))
    
    def _play_audio_cue(self, sound_path: str):
        """Plays an audio file if the library and file exist."""
        if playsound and os.path.exists(sound_path):
            try: playsound(sound_path, block=False)
            except Exception as e: logging.warning(f"Could not play audio cue {sound_path}: {e}")

    ### <<< START OF THE KEY FIX: The superior "overlap" logic >>>
    def _generate_and_speak_response(self, prompt: str):
        """Handles the full interaction cycle without pre-emptively stopping the recognizer."""
        print("\n> Solace is thinking...")
        
        # NOTE: We NO LONGER call stop_keyword_recognition here.
        
        try:
            self.is_speaking = True
            
            # 1. Proceed directly to the API call.
            system_instruction = f"{self.config.BASE_SYSTEM_PROMPT}\nCurrent date and time is {datetime.now().strftime('%A, %B %d, %Y, %I:%M %p')}."
            history = self.conversation_manager.get_history()
            user_prompt_part = types.Part.from_text(text=prompt)
            contents_for_api = history + [types.Content(role='user', parts=[user_prompt_part])]
            request_config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=self.available_tools,
            )
            response = self.genai_client.models.generate_content(
                model=self.config.GEMINI_MODEL_NAME,
                contents=contents_for_api,
                config=request_config,
            )
            
            # 2. Speak the response. This will interrupt the recognizer's audio stream,
            #    triggering the _canceled_handler, which we now handle gracefully.
            full_response_text = response.text
            print(f"  [Response] -> {full_response_text}")
            self._stream_text_to_speaker(full_response_text)
            
            # 3. Update history.
            self.conversation_manager.add_turn("user", [user_prompt_part])
            self.conversation_manager.add_turn("model", response.candidates[0].content.parts)

        except Exception as e:
            logging.error(f"Error during AI response generation: {e}", exc_info=True)
            error_message = "I'm sorry, I ran into a problem. Please try again."
            print(f"\n{error_message}")
            self._speak_text(error_message)
        finally:
            self._play_audio_cue(self.config.END_OF_RESPONSE_SOUND_PATH)
            self.is_speaking = False
            
            # 4. GUARANTEED RESTART: After TTS is done, restart the keyword recognizer.
            #    A tiny delay can help ensure the audio device is fully released.
            time.sleep(0.1)
            print("  [State] -> Resuming keyword detection.")
            self.speech_recognizer.start_keyword_recognition(self.keyword_model)
            print(f"\nSay '{self.config.KEYWORD}' to speak again.")
    ### <<< END OF THE KEY FIX >>>

    def _stream_text_to_speaker(self, text: str):
        """Splits text into sentences and speaks them sequentially."""
        sentence_buffer = ""
        delimiters = ".!?"
        for char in text:
            sentence_buffer += char
            if char in delimiters:
                self._speak_text(sentence_buffer.strip())
                sentence_buffer = ""
        if sentence_buffer.strip():
            self._speak_text(sentence_buffer.strip())

    def _speak_text(self, text: str):
        """Synthesizes and speaks the given text, handling errors."""
        if not text: return
        try:
            result = self.speech_synthesizer.speak_text_async(text).get()
            if result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logging.error(f"TTS Canceled: {cancellation.reason} ({cancellation.error_details})")
        except Exception as e:
            logging.error(f"Error during speech synthesis: {e}")

    # --- Event Handlers (RESTORED) ---
    def _recognized_handler(self, evt: speechsdk.SpeechRecognitionEventArgs):
        if self.is_speaking:
            return
            
        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print(f"\n>>> Keyword '{self.config.KEYWORD}' recognized. Listening...")
            self._play_audio_cue(self.config.ACTIVATION_SOUND_PATH)
        elif result.reason == speechsdk.ResultReason.RecognizedSpeech and result.text:
            user_query = result.text
            print(f"\n<<< You said: \"{user_query}\"")
            self._generate_and_speak_response(user_query)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            logging.warning("No speech recognized after keyword.")

    def _canceled_handler(self, evt: speechsdk.SpeechRecognitionEventArgs):
        """Handles recognition cancellations gracefully."""
        details = evt.cancellation_details
        if details.reason == speechsdk.CancellationReason.EndOfStream:
            logging.info("Recognition canceled gracefully (EndOfStream). This is normal.")
        elif details.reason == speechsdk.CancellationReason.Error:
            logging.error(f"Recognition CANCELED due to error: {details.error_details}")

    def _session_stopped_handler(self, evt: speechsdk.SessionEventArgs):
        """Logs when the recognition session stops."""
        logging.info(f"Recognition session stopped (ID: {evt.session_id}).")

    # --- Public Methods (RESTORED) ---
    def start(self):
        """Starts the main keyword recognition loop."""
        print(f"Say '{self.config.KEYWORD}' to activate the assistant.")
        self.speech_recognizer.start_keyword_recognition(self.keyword_model)
        try:
            while True: time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nStopping assistant...")
        finally:
            self.stop()

    def stop(self):
        """Stops the keyword recognizer."""
        print("Finalizing shutdown...")
        self.speech_recognizer.stop_keyword_recognition()
        print("Recognition stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    try:
        app_config = Config()
        assistant = VoiceAssistant(app_config)
        assistant.start()
    except Exception as e:
        logging.critical(f"Failed to start the assistant: {e}", exc_info=True)
        sys.exit(1)