#!/bin/bash
# Start OCR monitoring service - checks every 15 minutes

LOG_FILE="/home/tayyabcheema777/ali/ocr_monitoring.log"

echo "Starting OCR monitoring service (checks every 15 minutes)..."
echo "[$(date)] OCR Monitoring Service Started" >> "$LOG_FILE"

# Run initial check
/home/tayyabcheema777/ali/ocr_scheduler.sh

# Schedule to run every 15 minutes using while loop
while true; do
    sleep 900  # 15 minutes = 900 seconds
    /home/tayyabcheema777/ali/ocr_scheduler.sh
done
