#export MAIL_SERVER=localhost
#export MAIL_PORT=8025
python -m smtpd -n -c DebuggingServer localhost:8025
