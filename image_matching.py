from skimage.metrics import structural_similarity as ssim
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from sqlite3 import Error
import cv2
import os

path_to_preprocessed = os.path.join(os.path.dirname(__file__), 'pre-processed')
path_to_processed = os.path.join(os.path.dirname(__file__), 'processed')
path_to_db = os.path.join(os.path.dirname(__file__), "data.db")
processed_list = os.listdir(path_to_processed)
preprocessed_list = os.listdir(path_to_preprocessed)

def match(img_path):
    try:
        im = Image.open(os.path.join(path_to_preprocessed, img_path))
        processed_list = os.listdir(path_to_processed)
    except:
        print("cant open")
        return

    if len(processed_list) == 0:
        im.save(os.path.join(path_to_processed, img_path))
        os.remove(os.path.join(path_to_preprocessed, img_path))
        return 1.0, img_path

    im_np = np.array(im)
    if len(processed_list) != 0:
        match = {}
        for img_test in processed_list:
            try:
                im_match = Image.open(os.path.join(path_to_processed, img_test))
                im_match = np.array(im_match)
                im_cpy = im_np.copy()
                s = ssim(im_cpy, im_match, multichannel=True)
                match[s] = img_test
            except Exception as e:
                print(e)
                pass
        m = max(match, key=float)
        im.save(os.path.join(path_to_processed, img_path))
        os.remove(os.path.join(path_to_preprocessed, img_path))
        return m, match[m]



def process():
    print("Running Image Matching algorithm")
    val = None

    # initializing query for creating table
    table_query = """ CREATE TABLE IF NOT EXISTS match ( 
                           id integer PRIMARY KEY,
                           confidence float NOT NULL,
                           original integer
                       ); """

    # init query
    init_query = """SELECT MAX(id) from match;"""

    # creating database connection and making sure the correct tables exist
    conn = None

    try:
        conn = sqlite3.connect(path_to_db)
        d = conn.cursor()
        d.execute(table_query)
        d.execute(init_query)
        val = d.fetchall()
    except Error as e:
        print(e)

    # variable to rename images by number
    if val[0][0] is not None:
        i = val[0][0]
    else:
        i = -1

    j = len(preprocessed_list)
    for image in preprocessed_list:
        num = int(image.split(".")[0])
        if num <= i:
            continue
        img_path = os.path.join(path_to_preprocessed, image)
    #Process Data
        similarity, img = match(image)
        matching_img = int(img.split(".")[0])
        data = [num] + [similarity] + [matching_img]
    #Store Data
        d = conn.cursor()
        d.execute("""INSERT INTO match VALUES(?,?,?)""", data)
        conn.commit()
        print(str(j)+" Jobs Remain")
        j -= 1

    conn.close()
process()