import fetcher_main.fetcher as fetch
import image_matching
import pre_process
import time
import os

def loop():
    while True:
        fetch.retrieve()
        pre_process.process()
        image_matching.process()
        print("Safe to close")
        time.sleep(100)
        os.system("cls")
        print("Running Code")
loop()