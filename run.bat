cd C:\workspace\Manim
@echo off
REM --------------------------------------
REM Manim Batch File: Render MP4 and GIF
REM --------------------------------------

REM Set Python file name
SET PYFILE=pj_AxisEdge\run.py

REM Set the Scene name to render
SET SCENE=MeasurementErrorLC

REM Set output folder
SET OUTPUT_DIR=pj_AxisEdge\output

REM Create output folder if it doesn't exist
IF NOT EXIST "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

REM -----------------------------
REM Render MP4 video
REM -----------------------------
echo Rendering MP4...
python -m manim %PYFILE% %SCENE% -p -qh --media_dir ./%OUTPUT_DIR%

REM -----------------------------
REM Render GIF animation
REM -----------------------------
echo Rendering GIF...
python -m manim %PYFILE% %SCENE% -p -ql --format=gif --media_dir ./%OUTPUT_DIR%

REM Done message
echo.
echo MP4 and GIF rendering completed! Output is in ./%OUTPUT_DIR% folder
pause