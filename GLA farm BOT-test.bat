@ECHO OFF
:server_start
echo.
echo =========================
echo Starting GLA farm BOT-test
echo =========================
echo.
python test.py
echo.
echo =========================
echo PRESS CTRL+C TO STOP BOT
echo =========================
echo.
timeout 5
goto server_start