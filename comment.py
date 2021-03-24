import sqlite3
import praw
import os
import csv

path_to_db = os.path.join(os.path.dirname(__file__), 'data.db')
REPLY_TEMPLATE = '''This might be a repost. It's image is {:.2f}% similar to {}'''
init_query = '''CREATE TABLE IF NOT EXISTS replied (id INT PRIMARY KEY); '''
search_query = '''SELECT id FROM pre_process WHERE ext_id = ?'''
check_query = '''SELECT * FROM replied'''

def process():
    print("Processing Replies")
    conn = sqlite3.connect(path_to_db)
    c = conn.cursor()
    c.execute(init_query)
    conn.commit()
    c.execute(check_query)
    tcheck = c.fetchall()
    check = []
    for col in tcheck:
        check.append(col[0])


    reddit = praw.Reddit(client_id='aVFs_elcBcouwg',
                         client_secret='xEVULnu-o7oU28BoxEqw13LrHkTntg',
                         user_agent='RepostBot',
                         username='ReponstBot',
                         password='Reponst123')

    subreddit = reddit.subreddit("final_projekt")
    for submission in subreddit.new(limit=50):
        c.execute(search_query, (submission.id, ))
        res = c.fetchall()
        if res != []:
            if res[0][0] not in check:

                c.execute("SELECT * FROM MATCH WHERE id = ?", (res[0][0], ))
                sim = c.fetchall()
                c.execute("SELECT ext_link FROM pre_process WHERE id = ?", (sim[0][2], ))
                elink = c.fetchall()
                similarity = sim[0][1]  # <---- confidence value should be here
                link = elink[0][0]  # <------ link of original should be here
                message = REPLY_TEMPLATE.format(similarity * 100, link)
                if similarity < 0.3:
                    message = "This post does not look like a repost."

                if len(submission.title.split()) > 0:
                    if ((submission.url.endswith(".png")) or (submission.url.endswith(".jpg"))):
                        submission.reply(message)

                    else:
                        submission.reply("No image found in the post")
                c.execute("INSERT INTO replied VALUES(?)", (res[0][0], ))
                conn.commit()
    print("Replied")