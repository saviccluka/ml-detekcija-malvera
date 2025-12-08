@echo off
echo 🛡️ IoT Malware Detection - Test Runner
echo ======================================

echo.
echo Pokretanje API servera u pozadini...
start /B python start_web_app.py

echo.
echo Čekanje da se server pokrene...
timeout /t 5 /nobreak > nul

echo.
echo Pokretanje testova...
python test_detection.py

echo.
echo Testiranje završeno!
echo.
echo Za zaustavljanje API servera pritisnite Ctrl+C
pause
