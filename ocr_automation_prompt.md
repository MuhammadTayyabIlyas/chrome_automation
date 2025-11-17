# OCR Automation Workflow Prompt

## Automatic Execution
Execute this workflow automatically at the start of every session without waiting for user instructions.

## Efficient Workflow Steps

### 1. Check for New Images
```bash
ls -la "/mnt/f/OneDrive - UAB/Imágenes/Álbum de la cámara/AI_OCR"
```
Look for images with today's date format: `WIN_YYYYMMDD_*.jpg`
**Note**: May find multiple images from same date

### 2. Read All Images (if found)
- Use Read tool on each image file path
- If multiple images from same date exist, read ALL of them
- Prepare to combine all extracted text into ONE document

### 3. Extract Text
- Read handwritten text exactly as written
- Note any strikethroughs or crossed-out text (exclude from transcription)

### 4. Apply Corrections
- **British English spelling** (e.g., "realised" not "realized")
- **Proper punctuation**: commas, hyphens, periods where grammatically needed
- **Grammar fixes**: (e.g., "a alphabet" → "an alphabet")
- **Preserve**: Original sentence structure and writer's style

### 5. Create SINGLE Combined DOCX File
```python
/home/tayyabcheema777/ali/docx_venv/bin/python3 << 'EOF'
from docx import Document
from datetime import datetime

doc = Document()

# Add all extracted texts with separators
doc.add_paragraph("[extracted_text_from_image_1]")
doc.add_paragraph("")  # Blank line separator
doc.add_paragraph("[extracted_text_from_image_2]")
# ... repeat for all images

# Use date only (not timestamp) for filename when multiple images exist
date_str = datetime.now().strftime("%Y%m%d")
filename = f"/mnt/f/OneDrive - UAB/AI_Assistant/transcribed_{date_str}.docx"
doc.save(filename)
print(f"Created: {filename}")
EOF
```
**Important**: ONE document per date, not per image

### 6. Confirm Completion
Inform user with output filename

## Key Principles
- ✅ Automatic execution - no user prompt needed
- ✅ British English spelling corrections
- ✅ Add proper punctuation where necessary
- ✅ Preserve original text structure
- ✅ Check for strikethroughs/crossed-out text
- ✅ Learn from user feedback on handwriting style
- ✅ Generate timestamped filenames
- ✅ **IMPORTANT**: Multiple images from same date → ONE combined document
- ❌ Do not ask for confirmation - just execute
- ❌ Do not create separate files for each image

## Learning from Feedback
When user provides corrections:
1. Note the specific letter/word misread
2. Analyze handwriting pattern (e.g., "c" vs "v" distinction)
3. Apply contextual understanding for ambiguous characters
4. Update recognition approach for similar cases

## Output Location
All .docx files → `/mnt/f/OneDrive - UAB/AI_Assistant/`

## Virtual Environment
Python docx library: `/home/tayyabcheema777/ali/docx_venv/bin/python3`

## Enhanced Features Implemented

### 4. Smart Document Naming
- Format: `transcribed_YYYYMMDD_FirstWords_Xpages.docx`
- Extracts first 3 words from content as preview
- Includes page count if multiple images
- Example: `transcribed_20251117_Comment_Table_Content_3pages.docx`

### 5. Backup System
- Processed images moved to: `AI_OCR/Processed/` subfolder
- Prevents reprocessing same images
- Keeps originals safe for reference
- Log file tracks all processed images: `processed_images.log`

### 6. Multi-page Detection
- Automatically detects multiple images from same date
- Adds "Page X of Y" headers in document
- Maintains logical flow between pages
- Combines all into single document

### 7. Text Formatting Preservation
- Numbered lists: Detects `1)`, `1.`, `1:` patterns
- Bullet points: Detects `-`, `•`, `*` markers
- Indentation: Preserves spacing (0.5 inch per 4 spaces)
- Paragraph structure maintained

### 8. OCR Confidence Scoring
- Calculates confidence based on text characteristics
- Flags uncertain extractions with `[OCR Confidence: X%]`
- Low confidence (<70%) includes reason
- Summary shows average confidence per document

### Scheduled Monitoring (Every 15 Minutes)
- Script: `start_ocr_monitoring.sh`
- Automatically checks for new images every 15 minutes
- Runs in background continuously
- Logs all activity to `ocr_monitoring.log`

## How to Start Monitoring
```bash
# Start the 15-minute monitoring service
/home/tayyabcheema777/ali/start_ocr_monitoring.sh &

# Or run single check manually
/home/tayyabcheema777/ali/ocr_scheduler.sh
```

## Log Files
- `ocr_processing.log` - Processing events and results
- `processed_images.log` - Tracks processed image filenames
- `ocr_monitoring.log` - Service status and schedule
