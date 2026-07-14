@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title CASimation Estimator Launcher

echo.
echo =========================================
echo       CASimation Estimator Launcher
echo =========================================
echo Repository: %CD%
echo.

if not exist "app.py" (
    echo ERROR: app.py was not found in %CD%.
    goto :error
)
if not exist "requirements.txt" (
    echo ERROR: requirements.txt was not found in %CD%.
    goto :error
)
if not exist "estimator" (
    echo ERROR: estimator folder was not found.
    goto :error
)
if not exist "data\parts.csv" (
    echo ERROR: data\parts.csv was not found.
    goto :error
)
if not exist "data\taxes.csv" (
    echo ERROR: data\taxes.csv was not found.
    goto :error
)

set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"
set "REQ_STAMP=%CD%\.venv\requirements.timestamp"

if not exist "%VENV_PYTHON%" (
    echo Creating virtual environment...
    where python >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python was not found on PATH.
        goto :error
    )
    python -m venv ".venv"
    if errorlevel 1 (
        echo ERROR: Failed to create the virtual environment.
        goto :error
    )
)

echo Python environment: %VENV_PYTHON%
"%VENV_PYTHON%" --version

"%VENV_PYTHON%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Initializing pip...
    "%VENV_PYTHON%" -m ensurepip --upgrade
    if errorlevel 1 goto :error
)

call :install_dependencies
if errorlevel 1 goto :error

echo.
echo Running startup health checks...
"%VENV_PYTHON%" -m estimator.health_check --root "%CD%"
if errorlevel 1 (
    echo.
    echo Startup health checks failed. CASimation was not launched.
    goto :error
)

echo.
echo Starting CASimation...
echo Browser URL: http://localhost:8501
echo Close this window or press Ctrl+C to stop the application.
echo.

"%VENV_PYTHON%" -m streamlit run "app.py"
if errorlevel 1 (
    echo.
    echo ERROR: CASimation stopped unexpectedly.
    goto :error
)
goto :end

:install_dependencies
set "INSTALL_REQUIRED=0"
if not exist "%REQ_STAMP%" (
    set "INSTALL_REQUIRED=1"
) else (
    for %%F in ("requirements.txt") do set "REQ_TIME=%%~tF"
    set /p OLD_REQ_TIME=<"%REQ_STAMP%"
    if not "%REQ_TIME%"=="%OLD_REQ_TIME%" set "INSTALL_REQUIRED=1"
)

if "%INSTALL_REQUIRED%"=="1" (
    echo Installing or updating dependencies...
    "%VENV_PYTHON%" -m pip install --upgrade pip
    if errorlevel 1 exit /b 1
    "%VENV_PYTHON%" -m pip install -r "requirements.txt"
    if errorlevel 1 exit /b 1
    for %%F in ("requirements.txt") do echo %%~tF>"%REQ_STAMP%"
) else (
    echo Dependencies are current.
)
exit /b 0

:error
echo.
echo CASimation could not be started.
echo Review the messages above, then press any key to close.
pause >nul
exit /b 1

:end
endlocal
