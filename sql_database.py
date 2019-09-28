import sqlite3
import sys

db = sqlite3.connect('Uno_user_database') #creates a file for database that connects to sql
global c
c = db.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, username TEXT,
                       password TEXT, email TEXT)
''')
def register():
    global u_name_r
    global u_password_r
    global u_email_r
    u_name_r = input("Enter a username: ")
    u_password_r = input("Enter a password: ")
    u_email_r = input("Enter an email: ")
    

    c.execute('''INSERT OR IGNORE INTO users (username,password,email)VALUES (?,?,?)''', (u_name_r, u_password_r, u_email_r))
    print("Your Account has now been registered. Welcome to UNO")
#c.execute("SELECT * FROM users");
#print(c.fetchall())
def login():
  login = False
  while login == False:
      c = db.cursor()
      c.execute('''SELECT user_id, username, password, email FROM users''')
      u_name_l = input("Enter your username: ")
      u_password_l = input("Enter your password: ")
      c.execute('''SELECT EXISTS (SELECT username, password FROM users WHERE username = ? AND password = ? LIMIT 1)''',(u_name_l, u_password_l,))
      accountcheck = c.fetchone()
      if accountcheck[0] == 1:
        print("Login successful")
        login == True
        break
          
      else:
        print("Login Failed, please try again")
        login == False
        continue



register()
login()
db.commit()
db.close()


