import sqlite3
from sqlite3 import Error
import os

path_to_db = os.path.join(os.path.dirname(__file__), "data.db")
query1 = """SELECT * FROM pre_process WHERE id = ?"""
query2 = """SELECT id FROM pre_process WHERE 
                    test1 <= ? AND test1 >= ? AND
                    test2 <= ? AND test2 >= ? AND
                    test3 <= ? AND test3 >= ? AND
                    test4 <= ? AND test4 >= ? AND
                    test5 <= ? AND test5 >= ? AND
                    test6 <= ? AND test6 >= ? AND
                    test7 <= ? AND test7 >= ? AND
                    test8 <= ? AND test8 >= ? AND
                    test9 <= ? AND test9 >= ? AND
                    test10 <= ? AND test10 >= ? AND
                    test11 <= ? AND test11 >= ? AND
                    test12 <= ? AND test12 >= ? ; 

                                                  """

def execute(img):
    try:
        conn = sqlite3.connect(path_to_db)
        c = conn.cursor()
        c.execute(query1, (img, ))
        res = c.fetchall()
        res = res[0][4:]
        new_res = []
        for val in res:
            new_res.append(val + 50)
            new_res.append(val - 50)

        c.execute(query2, new_res)
        res = c.fetchall()
        new_res = []
        for val in res:
            new_res.append(val[0])
        return new_res
    except Error as e:
        print(e)
