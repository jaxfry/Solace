import subprocess
import re
import logging

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
                    logging.info(f"Found USB microphone: {card['name']} on {device_name}")
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
                    logging.info(f"Found USB speaker/DAC: {card['name']} on {device_name}")
                    return device_name
            except subprocess.CalledProcessError:
                continue
    
    logging.warning("No USB speaker/DAC found, will use default")
    return None

def find_audio_devices():
    """Find both USB microphone and speaker devices."""
    return {
        'microphone': find_usb_microphone(),
        'speaker': find_usb_speaker()
    }

if __name__ == "__main__":
    # Test the functions
    print("Audio Cards:")
    cards = get_audio_cards()
    for card in cards:
        print(f"  Card {card['number']}: {card['name']} [{card['id']}] - {card['type']}")
    
    print(f"\nUSB Microphone: {find_usb_microphone()}")
    print(f"USB Speaker/DAC: {find_usb_speaker()}")
