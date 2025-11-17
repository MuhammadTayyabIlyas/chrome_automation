#!/usr/bin/env python3
"""
Text-to-Speech script using ElevenLabs API
"""
import os
import sys
import subprocess
from pathlib import Path
from elevenlabs import ElevenLabs, save

# Load .env file if it exists
def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

def speak_text(text, api_key=None):
    """
    Convert text to speech using ElevenLabs API

    Args:
        text: The text to convert to speech
        api_key: ElevenLabs API key (if not set in environment)
    """
    # Get API key from parameter or environment variable
    if api_key is None:
        api_key = os.getenv('ELEVEN_API_KEY')

    if not api_key:
        print("Error: ElevenLabs API key not found!")
        print("Please create a .env file with your ELEVEN_API_KEY")
        print("You can copy .env.example to .env and add your API key there")
        print("Get your API key from: https://elevenlabs.io/app/settings/api-keys")
        sys.exit(1)

    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=api_key)

    # Generate audio
    print("Generating speech...")
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Default voice (Rachel)
        model_id="eleven_monolingual_v1"
    )

    # Save audio to file
    output_file = "output.mp3"
    print(f"Saving audio to {output_file}...")
    save(audio, output_file)

    # Play the audio using system player
    print("Playing audio...")
    try:
        # Try different audio players available on Linux
        players = ['mpg123', 'ffplay', 'mpv', 'vlc', 'aplay']
        for player in players:
            if subprocess.run(['which', player], capture_output=True).returncode == 0:
                subprocess.run([player, output_file], check=True)
                break
        else:
            print(f"Audio saved to {output_file}")
            print("No audio player found. Please install mpg123, ffplay, mpv, or vlc to play audio.")
    except Exception as e:
        print(f"Audio saved to {output_file}")
        print(f"Could not play automatically: {e}")

    print("Done!")

if __name__ == "__main__":
    # The programmer joke
    joke = """A programmer's wife asks him to go to the store and says, "Buy a gallon of milk, and if they have eggs, get a dozen."

He comes back with 12 gallons of milk.

His wife stares at the bags in disbelief and asks, "Why on earth did you buy 12 gallons of milk?!"

He replies, "They had eggs."

The next day, his wife, determined to be clearer, says: "Okay, go back to the store. Buy ONE gallon of milk. If they have eggs, buy SIX eggs. Got it?"

He comes back with one gallon of milk and six dozen eggs.

She sighs deeply. "What happened this time?"

He says, "Well, you said buy ONE gallon of milk, which I did. Then you said IF they have eggs—which evaluated to TRUE—buy SIX eggs. But you didn't specify the unit, and eggs come in dozens, so I interpreted SIX as the quantity and DOZEN as the default unit type for eggs!"

She looks at him and says, "I'm writing the shopping list in Python from now on."

He replies, "Make sure you use type hints."
"""

    # Check if custom text provided as command line argument
    if len(sys.argv) > 1:
        text_to_speak = " ".join(sys.argv[1:])
    else:
        text_to_speak = joke

    speak_text(text_to_speak)
