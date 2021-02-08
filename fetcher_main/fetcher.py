import praw
import sys, os, glob, shutil
import urllib.request
import sqlite3
import time


def retrieve():
    #Connect to raw.db
    conn = sqlite3.connect('raw.db')
    print("Opened database successfully")
    cursor = conn.cursor()

    #Create Table DETAILS
    conn.execute('''CREATE TABLE IF NOT EXISTS DETAILS
             (ID TEXT PRIMARY KEY     NOT NULL,
             TITLE           TEXT    NOT NULL,
             URL             TEXT    NOT NULL,
             CREATED         INT     NOT NULL); ''')

    #Initialize RedditBot
    reddit = praw.Reddit(client_id='aVFs_elcBcouwg',
                         client_secret='xEVULnu-o7oU28BoxEqw13LrHkTntg',
                         user_agent='RepostBot',
                         username='ReponstBot',
                         password='Reponst123')


    #Choose subreddit to download images
    subreddit = reddit.subreddit('images')
    top_subreddit = subreddit.new(limit=25)

    for submission in top_subreddit:

        print(type(submission.id))
        cursor.execute("SELECT ID FROM DETAILS WHERE ID = ?", (submission.id,))
        data = cursor.fetchall()

        if len(data) != 0:
            break
        elif ((submission.url.endswith(".png")) or (submission.url.endswith(".jpg"))):
        #Insert details in DB
            cursor.execute("INSERT INTO DETAILS (ID, TITLE, URL, CREATED) VALUES (?, ?, ?, ?)",
              (submission.id, submission.title, submission.url, submission.created));
            print("ADDED VALUES")

        #Select only .png and .jpg files to download
            if ((submission.url.endswith(".png")) or (submission.url.endswith(".jpg"))):
                name = submission.id + ".jpg"
            else:
                continue

        #Download images
            urllib.request.urlretrieve(submission.url, name)

    conn.commit()
    conn.close()

    os.system("MoveImages.py 1")

    #To make to code loop after specific interval
    """while True:
        #Your script here
        time.sleep(Amount of time in seconds)"""

def loop():
    while exit != 1:
        retrieve()
        time.sleep(15) #seconds

if __name__ == '__main__':
    loop()
    
