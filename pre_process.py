import os
from PIL import Image
import cv2
import numpy as np
import sqlite3
import sys
from sqlite3 import Error

def remove(path):
    os.remove(path)
    pass

def process():
    print("Running Pre-processor")

    # initializing paths
    path_to_raw = os.path.join(os.path.dirname(__file__), 'fetcher_main\\Images')
    path_to_preprocessed = os.path.join(os.path.dirname(__file__), 'pre-processed')
    path_to_rawdb = os.path.join(os.path.dirname(__file__), 'data.db')
    path_to_db = os.path.join(os.path.dirname(__file__), "data.db")
    raw_list = os.listdir(path_to_raw)

    # number of subdivisions for each image
    slices = 2

    # initializing query for creating table
    table_query = """ CREATE TABLE IF NOT EXISTS pre_process ( 
                        id integer PRIMARY KEY,
                        ext_id text NOT NULL UNIQUE,
                        ext_link text NOT NULL,
                        ext_timestamp integer NOT NULL,
                        test1 integer NOT NULL,
                        test2 integer NOT NULL,
                        test3 integer NOT NULL,
                        test4 integer NOT NULL,
                        test5 integer NOT NULL,
                        test6 integer NOT NULL,
                        test7 integer NOT NULL,
                        test8 integer NOT NULL,
                        test9 integer NOT NULL,
                        test10 integer NOT NULL,
                        test11 integer NOT NULL,
                        test12 integer NOT NULL
                    ); """

    # init query
    init_query = """SELECT MAX(id) from pre_process;"""
    init_query_raw = """SELECT * from DETAILS WHERE ID = ?"""

    # creating database connection and making sure the correct tables exist
    conn = None
    conn_raw = None

    try:
        conn = sqlite3.connect(path_to_db)
        conn_raw = sqlite3.connect(path_to_rawdb)
        c = conn.cursor()
        r = conn_raw.cursor()
        c.execute(table_query)
        c.execute(init_query)
        val = c.fetchall()
    except Error as e:
        print(e)

    # variable to rename images by number
    if val[0][0] is not None:
        i = val[0][0] + 1
    else:
        i = 0

    job_counter = len(raw_list)
    for image in raw_list:
        path = os.path.join(path_to_raw, image)
        try:
            im = Image.open(path)
            query_var = image.split(".")[0]
            r.execute(init_query_raw, (query_var,))
            raw = r.fetchall()
        except:
            print("image did not open")
            job_counter -= 1
            remove(os.path.join(path_to_raw, image))
            continue
        im.convert("RGB")

        # resizing done here
        size = (600, 600)
        im = im.resize(size)

        # processing for database done here
        im2 = np.array(im)
        if im2.shape[-1] == 2:
            print("gray with alpha")
            job_counter -= 1
            remove(os.path.join(path_to_raw, image))
            continue
        if len(im2.shape) == 2:
            im2 = cv2.cvtColor(im2, cv2.COLOR_GRAY2RGB)
        h, w = im2.shape[0] / slices, im2.shape[1] / slices
        im_arr = []
        for j in range(0, slices):
            for k in range(0, slices):
                avg_img = im2[int(h * j):int(h * (j + 1)), int(w * k):int(w * (k + 1))]
                average = avg_img.mean(axis=0).mean(axis=0).astype(int)
                average = average.tolist()
                try:
                    im_arr.append(average[0:3])
                except:
                    job_counter -= 1
                    remove(os.path.join(path_to_raw, image))
                    continue

        flatten_list = lambda y: [x for a in y for x in flatten_list(a)] if type(y) is list else [y]
        im_arr = flatten_list(im_arr)
        db_arr = [i] + [raw[0][0], raw[0][2], raw[0][3]] + im_arr
        # database query here
        try:

            c = conn.cursor()
            c.execute("""INSERT INTO pre_process VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", db_arr)
            conn.commit()
        except Error as e:
            job_counter -= 1
            remove(os.path.join(path_to_raw, image))
            continue
        try:
            im.save(os.path.join(path_to_preprocessed, str(i)) + ".jpg")
        except OSError:
            im = im.convert("RGB")
            im.save(os.path.join(path_to_preprocessed, str(i)) + ".jpg", "JPEG", quality=100)
        i += 1
        remove(os.path.join(path_to_raw, image))
        job_counter -= 1
        print(str(job_counter) + " Tasks Remain")

    conn.close()
    conn_raw.close()
    print("Pre-Process Complete")
