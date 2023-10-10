import random
import string
import datetime
from time import sleep

def generate_random_log():
    while True:
        timestamp = datetime.datetime.utcnow().isoformat()
        level = random.choice(("INFO", "ERROR", "WARNING"))
        message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
        crawler_id = random.randint(10000, 99999)
        status = random.choice(("running", "stopped", "paused"))

        log = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "crawler_id": crawler_id,
            "status": status
        }

        yield {'data': log}
        sleep(0.5)


def generate_random_chart():
    while True:
        yield {'data': random.randint(0, 99)}