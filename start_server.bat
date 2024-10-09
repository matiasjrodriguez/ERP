@echo off
call venv\Scripts\activate
start http://127.0.0.1:8000
title La Milagrosa
uvicorn main:app --reload
timeout /t 2 /nobreak >nul