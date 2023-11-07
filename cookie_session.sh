while [[ true ]]; do
  python3 start_session_from_cookies_win32.py $@
  echo "**************** Completed Session `date` ****************"
done
