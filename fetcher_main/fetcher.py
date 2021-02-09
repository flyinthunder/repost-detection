#! python3

import praw
import sys, os, glob, shutil
import urllib.request
import sqlite3
import time
import keyboard
import fetcher_main.move_images as move_images

exit = 0

def retrieve():
    #Connect to test.db
    conn = sqlite3.connect('data.db')
    print("Opened database successfully")
    cursor = conn.cursor()

    #Create Table DETAILS
    conn.execute('''CREATE TABLE IF NOT EXISTS DETAILS 
             (ID INT PRIMARY KEY     NOT NULL,
             TITLE           TEXT    NOT NULL,
             URL             TEXT    NOT NULL,
             CREATED         INT     NOT NULL); ''')

    #Checking if the user pressed 'q'
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            exit = 1

    #Initialize RedditBot
    reddit = praw.Reddit(client_id='aVFs_elcBcouwg',
                         client_secret='xEVULnu-o7oU28BoxEqw13LrHkTntg',
                         user_agent='RepostBot',
                         username='ReponstBot',
                         password='Reponst123')


    #Choose subreddit to download images
    subreddit = reddit.subreddit('final_projekt')
    top_subreddit = subreddit.new(limit=25)

    for submission in top_subreddit:

        print(submission)
        cursor.execute("SELECT ID FROM DETAILS WHERE ID = ?", (submission.id,))
        data = cursor.fetchall()

        if len(data) != 0:
            continue
        elif ((submission.url.endswith(".png")) or (submission.url.endswith(".jpg"))):
        #Insert details in DB
            cursor.execute("INSERT INTO DETAILS (ID, TITLE, URL, CREATED) VALUES (?, ?, ?, ?)",
              (submission.id, submission.title, submission.url, submission.created))
            print("ADDED VALUES")

        #Select only .png and .jpg files to download
            if submission.url.endswith(".png"):
                name = submission.id + ".png"
            elif submission.url.endswith(".jpg"):
                name = submission.id + ".jpg"
            else:
                continue
        #Download images
            urllib.request.urlretrieve(submission.url, name)

    conn.commit()
    conn.close()

    move_images.move()

    #To make to code loop after specific interval
    """while True:
        #Your script here
        time.sleep(Amount of time in seconds)"""

def loop():
    global exit
    while exit != 1:
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            exit = 1
        retrieve()
        time.sleep(45) #seconds


