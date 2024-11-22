from fastapi import FastAPI, WebSocket, WebSocketException,Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from pydantic import BaseModel
import uvicorn




app=FastAPI()

conn=sqlite3.connect('app.db')
c=conn.cursor()
c.execute('Create table if not exists user(id integer primary key AUTOINCREMENT,username text,email text,password text)')
c.execute('Create table if not exists message(id integer primary key AUTOINCREMENT, sender text not null, message text not null, timestamp DATATIME default CURRENT_TIMESTAMP)')
c.execute('create table if not exists groups (id integer primary key AUTOINCREMENT, name text not null unique, created_by text not null, created_at DATETIME default CURRENT_TIMESTAMP)')
c.execute('create table if not exists membership(id integer primary key AUTOINCREMENT, group_id integer not null, user_id integer nt null, joined_at DATATIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (group_id) references groups(id),foreign key(user_id) references user(id))')
conn.commit()
conn.close()

class User(BaseModel):

    username:str
    email:str
    password:str

@app.post('/add')
def add(user:User):
    conn=sqlite3.connect('app.db')
    cursor=conn.cursor()
    cursor.execute('insert into user(username,email,password) values(?,?,?)',(user.username,user.email,user.password))
    conn.commit()
    conn.close()
    return {'message':'user added'}
        

@app.get('/')
def get_users():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username,password FROM user')
    users = cursor.fetchall()
    conn.close()
    return {'users': users}

@app.delete('/delete')
def delete_user(username,password):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user WHERE username=? AND password=?',(username,password))
    conn.commit()
    conn.close()
    return {'message':'user deleted'}

@app.put('/update')
def update_user(email,password,username):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE user SET email=? AND password=? where username=?',(email,password,username))
    conn.commit()
    conn.close()
    return {'message':'user updated'}
if __name__=='__main__':
    uvicorn.run(app,host='127.0.0.1',port=8001)