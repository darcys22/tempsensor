
all:
	/usr/bin/python3 sensor.py

start:
	pm2 start /home/pi/tempsensor/sensor.py --name temp --no-autorestart --interpreter python3 --cron "*/15 * * * *"

stop:
	pm2 stop temp
