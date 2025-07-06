import os
import struct
import wave
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

import pvporcupine
from pvrecorder import PvRecorder

import numpy as np
import whisper
import warnings

from google import genai
from google.genai import types

import pyttsx3  


def record_until_silence(
    recorder,
    sample_rate=16000,
    silence_threshold=20,      
    min_silence_frames=15,     
    max_record_seconds=10,
    min_voice_frames=3,
    debug_rms=False            
):
    frames = []
    silence_count = 0
    voice_count = 0
    total_frames = 0
    max_frames = int(sample_rate / recorder.frame_length * max_record_seconds)
    print("Listening for speech...")

    while True:
        pcm = recorder.read()
        frames.append(pcm)
        total_frames += 1

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            arr = np.array(pcm, dtype=np.int16)
            rms = np.sqrt(np.mean(np.square(arr))) if arr.size > 0 else 0
            if np.isnan(rms):
                rms = 0.0

        if debug_rms:
            print(f"RMS: {rms:.2f} | Voice Frames: {voice_count} | Silence Frames: {silence_count}")

        if rms < silence_threshold:
            if voice_count > min_voice_frames:
                silence_count += 1
        else:
            silence_count = 0
            voice_count += 1

        if silence_count >= min_silence_frames:
            print("Silence detected, stopping recording.")
            break

        if total_frames >= max_frames:
            print("Max recording time reached.")
            break

    audio = np.concatenate(frames).astype(np.int16).tobytes()
    return audio


def transcribe_with_whisper(audio_bytes, sample_rate=16000):
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        with wave.open(tmp_wav, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_bytes)
        wav_path = tmp_wav.name

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
        model = whisper.load_model("small.en")
        result = model.transcribe(wav_path)
    os.remove(wav_path)
    return result["text"]

GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_SYSTEM_PROMPT = (
    "You are Solace, a helpful voice assistant for the Solace device. "
    "Answer user questions clearly and concisely. "
    "Do not talk too much if not required. "
    "If a short answer suffices, keep your response brief."
)

def ask_gemini(prompt, model="gemini-2.5-flash"):
    response = client.models.generate_content(
        model=model,
        contents=[
            GEMINI_SYSTEM_PROMPT,
            prompt
        ]
    )
    return response.text


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def main():
    access_key = os.environ.get("PVPORCUPINE_ACCESS_KEY")
    keywords = ["porcupine"]
    keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in keywords]
    sensitivities = [0.5] * len(keyword_paths)
    audio_device_index = -1
    output_path = None

    try:
        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=keyword_paths,
            sensitivities=sensitivities)
    except pvporcupine.PorcupineInvalidArgumentError as e:
        print("One or more arguments provided to Porcupine is invalid.")
        print(e)
        raise e
    except pvporcupine.PorcupineActivationError as e:
        print("AccessKey activation error")
        raise e
    except pvporcupine.PorcupineActivationLimitError as e:
        print("AccessKey has reached its temporary device limit")
        raise e
    except pvporcupine.PorcupineActivationRefusedError as e:
        print("AccessKey refused")
        raise e
    except pvporcupine.PorcupineActivationThrottledError as e:
        print("AccessKey has been throttled")
        raise e
    except pvporcupine.PorcupineError as e:
        print("Failed to initialize Porcupine")
        raise e

    keywords_print = []
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords_print.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords_print.append(keyword_phrase_part[0])

    print('Porcupine version: %s' % porcupine.version)

    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=audio_device_index)
    recorder.start()

    wav_file = None
    if output_path is not None:
        wav_file = wave.open(output_path, "w")
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)

    print('Listening ... (press Ctrl+C to exit)')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if wav_file is not None:
                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

            if result >= 0:
                print('[%s] Detected %s' % (str(datetime.now()), keywords_print[result]))
                audio_bytes = record_until_silence(recorder, debug_rms=False)
                print("Transcribing...")
                try:
                    text = transcribe_with_whisper(audio_bytes)
                    print("Transcription:", text)
                    gemini_response = ask_gemini(text)
                    print("Gemini:", gemini_response)
                    speak(gemini_response)
                except Exception as e:
                    print("Transcription or Gemini failed:", e)
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        if wav_file is not None:
            wav_file.close()


if __name__ == '__main__':
    main()