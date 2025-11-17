#!/usr/bin/env python3
from gtts import gTTS
import os

# The joke text
joke = """Why did the PhD student bring a ladder to the library?

Because they heard finishing a PhD requires reaching new heights of understanding, but they're still stuck on the first step of their literature review!

Don't worry, at least you're not alone. Every PhD student is simultaneously convinced they're the only one who has no idea what they're doing AND that everyone else has it all figured out!"""

# Create the TTS object with English language
tts = gTTS(text=joke, lang='en', slow=False)

# Save to MP3 file
output_file = '/home/tayyabcheema777/ali/phd_joke.mp3'
tts.save(output_file)

print(f"MP3 file created: {output_file}")

# Play the file using available audio player
try:
    os.system(f'ffplay -nodisp -autoexit "{output_file}" 2>/dev/null || mpg123 "{output_file}" 2>/dev/null || vlc "{output_file}" 2>/dev/null')
except:
    print("Audio file created but couldn't play automatically. You can play it manually.")
