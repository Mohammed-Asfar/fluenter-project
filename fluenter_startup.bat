@echo off
echo Starting Fluenter Service...
cd /d D:\Programs\AI Agents\fluenter-project
start chrome
uv run fluenter_app.py
