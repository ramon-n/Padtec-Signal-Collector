@echo off
title Padtec Path Monitor v4.0
echo ========================================
echo   Iniciando Padtec Path Monitor v4.0
echo ========================================
echo.

set PYTHON_EXE="%LocalAppData%\Programs\Python\Python312\python.exe"

if exist %PYTHON_EXE% (
    %PYTHON_EXE% start.py
) else (
    echo [ERRO] Python 3.12 nao encontrado em: %PYTHON_EXE%
    echo Por favor, verifique a instalacao do Python.
    pause
)
