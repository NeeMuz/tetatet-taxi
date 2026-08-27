@echo off
cd /d %~dp0..
echo [1/2] Screenshots (server must be on :8000)...
python docs\capture_screenshots.py
echo [2/2] PDF...
python docs\build_pdf.py
echo Ready: docs\Tetatet_Project_Description.pdf
