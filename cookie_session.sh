while [[ true ]]; do
  python3 start_windows32_cookie_session.py $@
  echo "**************** Completed Session `date` ****************"
done
