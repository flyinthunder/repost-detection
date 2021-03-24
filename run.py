import fetcher_main.fetcher as fetch
import image_matching
import pre_process
import comment
import time
import os

txt = "Waiting for {} more seconds"
wait = 5
number = 5
def loop():
    print("Running Code")
    while True:
        fetch.retrieve()
        pre_process.process()
        image_matching.process()
        comment.process()
        print("Safe to close")
        for i in range(number, 1, -1):
            print(txt.format(i*wait))
            time.sleep(wait)
        os.system("cls")
loop()