import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")
cursor = conn.cursor()




"""conn.execute('''CREATE TABLE DETAILS
         (ID INT PRIMARY KEY     NOT NULL,
         TITLE           TEXT    NOT NULL,
         URL            TEXT     NOT NULL,
         TIME           INT      NOT NULL); ''')"""

print("CREATED TABLE DETAILS")

"""name = 7
cursor.execute("INSERT INTO DETAILS (ID, TITLE, URL, TIME) VALUES (?, ?, ?, ?)",
          (name, name, name, name));
print("ADDED VALUES")"""

name = 10
cursor.execute("SELECT rowid FROM DETAILS WHERE ID = ?", (name,))
data=cursor.fetchall()

if len(data) == 0:
        print('There is no component named %s'%name)

cursor.execute("SELECT count(URL) FROM DETAILS")
print(cursor.fetchall())

conn.commit()        
conn.close()

#select * FROM Table details where ID == submission  
