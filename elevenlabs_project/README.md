# ElevenLabs Text-to-Speech Project

This project uses ElevenLabs API to convert text to speech.

## Setup

1. **Create your `.env` file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your ElevenLabs API key to `.env`:**
   - Get your API key from: https://elevenlabs.io/app/settings/api-keys
   - Open `.env` and replace `your_api_key_here` with your actual API key

3. **Install dependencies (already done):**
   The virtual environment is already set up with ElevenLabs SDK installed.

## Usage

### Read the default joke:
```bash
elevenlabs_venv/bin/python text_to_speech.py
```

### Speak custom text:
```bash
elevenlabs_venv/bin/python text_to_speech.py "Your custom text here"
```

## Files

- `text_to_speech.py` - Main script for text-to-speech conversion
- `elevenlabs_venv/` - Python virtual environment with dependencies
- `.env` - Your API configuration (create from `.env.example`)
- `.env.example` - Template for environment variables
- `.gitignore` - Git ignore file (protects your API key from being committed)
