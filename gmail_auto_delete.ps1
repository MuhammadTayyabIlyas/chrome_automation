# Gmail Auto Delete - PowerShell Script for Windows
# This script clicks Select All checkbox and Delete button in Gmail
# UPDATED with precise coordinates from ui-element-locator

Write-Host ""
Write-Host "================================================================"
Write-Host "  Gmail Auto Delete - PowerShell Automation (PRECISE)"
Write-Host "================================================================"
Write-Host ""
Write-Host "This script will:"
Write-Host "  1. Click Select All checkbox at (506, 381)"
Write-Host "  2. Wait 2 seconds"
Write-Host "  3. Click 'Select all conversations' link at (600, 410)"
Write-Host "  4. Wait 2 seconds"
Write-Host "  5. Click Delete button at (777, 376)"
Write-Host ""
Write-Host "Coordinates VERIFIED by user observation!"
Write-Host "Make sure Gmail is open and visible!"
Write-Host ""

# Load Windows Forms for mouse control
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class Mouse {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);

    public const uint MOUSEEVENTF_LEFTDOWN = 0x02;
    public const uint MOUSEEVENTF_LEFTUP = 0x04;
}
"@

# Countdown
Write-Host "Starting in 3 seconds..."
for ($i = 3; $i -gt 0; $i--) {
    Write-Host "  $i..."
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "============================================================"

# Step 1: Click Select All checkbox (VERIFIED COORDINATES)
Write-Host "[STEP 1] Moving cursor to Select All checkbox (506, 381)..."
[Mouse]::SetCursorPos(506, 381)
Start-Sleep -Milliseconds 500

Write-Host "[STEP 1] Clicking Select All checkbox..."
[Mouse]::mouse_event([Mouse]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
[Mouse]::mouse_event([Mouse]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
Write-Host "[STEP 1] Select All checkbox clicked!" -ForegroundColor Green

# Wait for selection
Write-Host "[WAIT] Waiting 2 seconds for emails to be selected..."
Start-Sleep -Seconds 2

# Step 2: Click "Select all conversations" link if it appears
Write-Host "[STEP 2] Clicking 'Select all conversations' link (600, 410)..."
[Mouse]::SetCursorPos(600, 410)
Start-Sleep -Milliseconds 500

Write-Host "[STEP 2] Clicking to select ALL conversations..."
[Mouse]::mouse_event([Mouse]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
[Mouse]::mouse_event([Mouse]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
Write-Host "[STEP 2] 'Select all' link clicked!" -ForegroundColor Green

Write-Host "[WAIT] Waiting 2 seconds..."
Start-Sleep -Seconds 2

# Step 3: Click Delete button (VERIFIED COORDINATES)
Write-Host "[STEP 3] Moving cursor to Delete button (777, 376)..."
[Mouse]::SetCursorPos(777, 376)
Start-Sleep -Milliseconds 500

Write-Host "[STEP 3] Clicking Delete button..."
[Mouse]::mouse_event([Mouse]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
[Mouse]::mouse_event([Mouse]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
Write-Host "[STEP 3] Delete button clicked!" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================"
Write-Host "[DONE] Automation completed!" -ForegroundColor Green
Write-Host "============================================================"
Write-Host ""
Write-Host "Check your Gmail to verify emails were deleted."
Write-Host ""
