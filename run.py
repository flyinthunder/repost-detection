import fetcher_main.fetcher as fetch
import image_matching
import pre_process
import time
import os

txt = "Waiting for {} more seconds"
def loop():
    print("Running Code")
    while True:
        fetch.retrieve()
        pre_process.process()
        image_matching.process()
        print("Safe to close")
        for i in range(10, 1, -1):
            print(txt.format(i*10))
            time.sleep(10)
        os.system("cls")
loop()