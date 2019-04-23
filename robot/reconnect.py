import os, requests
from time import sleep


# This file automatically reconnects the wifi on the pi if it drops, used for LOS tests
# DO NOT RUN THIS FILE WITHOUT A & AT THE END OF THE FILE BECAUSE THERE IS AN INFINITE LOOP SO THE REST OF THE SYSTEM WON'T START I ALREADY MADE THIS MISTAKE PLEASE DON'T DO IT AGAIN

while True:
    try:
        r = requests.get('http://google.com')
        if (r.status_code == 200):
            pass
        else:
            os.system('sudo sh reconnect.sh')
        sleep(5)
    except (requests.exceptions.ConnectionError):
        os.system('sudo sh reconnect.sh')