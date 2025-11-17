#!/bin/bash
# OCR Automation Scheduler - Runs every 15 minutes

OCR_FOLDER="/mnt/f/OneDrive - UAB/Imágenes/Álbum de la cámara/AI_OCR"
OUTPUT_FOLDER="/mnt/f/OneDrive - UAB/AI_Assistant"
PROCESSED_FOLDER="$OCR_FOLDER/Processed"
LOG_FILE="/home/tayyabcheema777/ali/ocr_processing.log"
PROCESSED_LOG="/home/tayyabcheema777/ali/processed_images.log"

# Create necessary folders
mkdir -p "$PROCESSED_FOLDER"
mkdir -p "$OUTPUT_FOLDER"

# Get today's date
TODAY=$(date +%Y%m%d)

# Find images with today's date that haven't been processed
NEW_IMAGES=$(find "$OCR_FOLDER" -maxdepth 1 -name "WIN_${TODAY}_*.jpg" -type f)

if [ -z "$NEW_IMAGES" ]; then
    echo "[$(date)] No new images found for $TODAY" >> "$LOG_FILE"
    exit 0
fi

# Count new images
IMAGE_COUNT=$(echo "$NEW_IMAGES" | wc -l)
echo "[$(date)] Found $IMAGE_COUNT new image(s) for processing" >> "$LOG_FILE"

# Trigger Python OCR processing script
/home/tayyabcheema777/ali/docx_venv/bin/python3 /home/tayyabcheema777/ali/ocr_processor.py

echo "[$(date)] Processing complete" >> "$LOG_FILE"
