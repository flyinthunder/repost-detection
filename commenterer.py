import sqlite3
import praw
import os
import csv

path_to_db = os.path.join(os.path.dirname(__file__), 'data.db')
REPLY_TEMPLATE = '''This might be a repost. It's image is {:.2f}% similar to {}'''
init_query = '''CREATE TABLE IF NOT EXISTS replied (id INT PRIMARY KEY); '''

def reply():
    pass


def process():

    conn = sqlite3.connect(path_to_db)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute(init_query)

    #Connecting reddit
    reddit = praw.Reddit(client_id='aVFs_elcBcouwg',
                         client_secret='xEVULnu-o7oU28BoxEqw13LrHkTntg',
                         user_agent='RepostBot',
                         username='ReponstBot',
                         password='Reponst123')

    subreddit = reddit.subreddit("final_projekt")

    c.execute("SELECT * from match WHERE confidence >= ?", (0,))
    d = c.fetchall()

    for row in d:
        if row[0] != 7:  #id from replied
            print(row[0])
            continue
        c.execute("SELECT confidence FROM match WHERE id == ?", (row[0],))
        conf = c.fetchall()
        c.execute("SELECT ext_link from pre_process WHERE id == ?", (row[2],))
        elink = c.fetchall()

        #Creating new list and csv file to store already replied post ids
        if not os.path.isfile("replied.csv"):
            replied = []
        else:
            with open("replied.csv", "r") as f:
                replied = f.read()
                replied = replied.split("\n")
                replied = list(filter(None, replied))

        #Submission in Reddit
        
        for submission in subreddit.new(limit=50):
            similarity = conf[0][0]  # <---- confidence value should be here
            link = elink[0][0]  # <------ link of original should be here
            message = REPLY_TEMPLATE.format(similarity * 100, link)
            #print(message)

            if submission.id not in replied:
                if len(submission.title.split()) > 0:
                    if ((submission.url.endswith(".png")) or (submission.url.endswith(".jpg"))):
                        submission.reply(message)
                        print("Replying to: ", submission.title)
                        replied.append(submission.id)  #Stores submission.id in "replied" list
                    else:
                        submission.reply("No image found in the post")
                        print("No image found in the post: ", submission.title)


            else:
                print("Already replied to post: ", submission.title)

        #Writing into csv file
        with open("replied.csv", "w") as f:
            for post_id in replied:
                f.write(post_id + "\n")

    #Entering data from csv file into database
    a_file = open('replied.csv')
    rows = csv.reader(a_file)
    c.executemany("INSERT OR IGNORE INTO replied (id) VALUES (?)", rows)
    d = c.execute("SELECT * FROM replied")
    #print(d.fetchall())

    conn.commit()
    conn.close()

process()