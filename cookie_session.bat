@echo off

newsession:
  python3 start_session_from_cookies_win32.py $@
  echo "**************** Completed Session ****************"
goto newsession

