import fetcher_main.fetcher as fetch
import image_matching
import pre_process
import time

def loop():
    while True:
        fetch.retrieve()
        pre_process.process()
        image_matching.process()
        time.sleep(30)
loop()