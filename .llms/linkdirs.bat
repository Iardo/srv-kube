@echo off
setlocal enabledelayedexpansion

set "root_dir=%~dp0.."

for %%a in (claude roo) do (
    if exist "%root_dir%\.%%a" rmdir "%root_dir%\.%%a"
    mklink /J "%root_dir%\.%%a" "%root_dir%\.llms" >nul
)

rem Claude Code only auto-loads CLAUDE.md from the project root
if exist "%root_dir%\CLAUDE.md" del /f /q "%root_dir%\CLAUDE.md"
mklink /H "%root_dir%\CLAUDE.md" "%root_dir%\.llms\AGENTS.md" >nul

endlocal
