from flask import Flask,request, jsonify
import mysql.connector
app=Flask(__name__)

con=mysql.connector.connect(user='root',passwd='123456', charset='utf8')
cur=con.cursor()
cur.execute("create database if not exists test character set utf8;")
cur.execute("use test")
cur.execute("create table if not exists"
            " user(username char(20),nickname char(20),password char(20),sex char(1))character set utf8;")
cur.execute("create table if not exists guestbook"
            "(content char(200),username char(20),nickname char(20),post_time timestamp(6),last_correct timestamp(6))"
            "character set utf8;")
cursor=con.cursor()

@app.route('/',methods=['GET'])
def board():
    value=cursor.fetchall()
    for x in value:
        content=x[0]
        nickname=x[2]
        post_time=x[3]
        last_correct=x[4]
        return board

@app.route('/guestbook',methods=['POST'])
def write():
    data=request.get_json(force=True)
    username=session.get('username')
    if username is None:
        raise HttpError(401, '请先登录')
    content=data.get('content')
    nickname=data.get('nickname')
    cursor.execute('insert into `guestbook`(`content`,`username`,`nickname`,`post_time`) values(%s,%s,%s,%s)',
                   (content,username,nickname,'now()'))
    con.commit()
    cursor.close()
    con.close()
    return "发表成功"

@app.route('/guestbook/content',methods=["PUT"])
def correct():
    data=request.get_json(force=True)
    username=session.get('username')
    content=data.get('content')
    if username is None:
        raise HttpError(401, '请先登录')
    cursor.execute('update `guestbook` set `content`=%s,last_correct=%s where username=%s and content=%s',
                   (content,'now()',username,board.get('content')))
    con.commit()
    cursor.close()
    con.close()
    return '修改成功'

@app.route('guestbook/deletion',methods=['DELETTE'])
def deletion():
    content=board.get('content')
    username=session.get('username')
    if username is None:
        raise HttpError(401, '请先登录')
    cursor.execute('delete `guestbook` set `content`=%s,last_correct=%s where username=%s and content=%s',(content, 'now()', username,content))
    con.commit()
    cursor.close()
    con.close()
    return '删除成功'

@app.route('/user', methods=['POST','GET'])
def register():
    data=request.get_json(force=True)
    username=data.get('username')
    nickname=data.get('nickname')
    password=data.get('password')
    sex=data.get("sex")
    cursor.execute('select count(*) from `user` where `username`=%s',(username,))
    count=cursor.fetchall()
    if count[0]>=1:
        raise HttpError(409, '用户名已存在')
    if username is None:
        raise  HttpError(400,"请输入username")
    if nickname is None:
        raise HttpError(400, "请输入nickname")
    if password is None:
        raise HttpError(400, "请输入password")
    if sex is None:
        raise HttpError(400, "请输入sex")
    cursor.execute('insert into `user`(`username`,`nickname`,`password`,`sex`) values (%s, %s,%s,%s)',(username, nickname, password, sex))
    con.commit()
    cursor.close()
    con.close()
    return '注册成功'



@app.route('/session', methods=['POST'])
def session():
    data=request.get_json(force=True)
    username=data.get('username')
    password=data.get('password')
    cursor.execute('select `username`, `password` from `user` where `username`=%s', (username,))
    values=cursor.fetchone()
    if values is None:
        raise HttpError(402, '用户名或密码错误')
    if username!=values[0] or password!=values[2]:
        raise HttpError(402, '用户名或密码错误')
    session['username']=username
    session['password']=password
    return '登录成功'


@app.route('/users/username', methods=['PUT'])
def change_username():
    data=request.get_json(force=True)
    username=data.get('username')
    if session.get('username') is None:
        raise HttpError(401, '请先登录')
    cursor.execute('select count(*) from `users` where `username`=%s', (username,))
    count=cursor.fetchone()[0]
    if count>=1:
        raise HttpError(409, '用户名已存在')
    cursor.execute('update `users` set `username`=%s where username=%s', (session.get('username'), username))
    con.commit()
    cursor.close()
    con.close()
    return '修改用户名成功'


@app.route('/users/password', methods=['PUT'])
def change_password():
    data=request.get_json(force=True)
    username=session.get('username')
    password=data.get('password')
    if session.get('password') is None:
        raise HttpError(401, '请先登录')
    cursor.execute('update `user` set `password`=%s where username=%s',(password,username))
    con.commit()
    cursor.close()
    con.close()
    return '修改密码成功'

class HttpError(Exception):
    def __init__(self, status_code, message):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            'status': self.status_code,
            'msg': self.message
        }
@app.errorhandler(HttpError)
def handle_http_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
if __name__ == '__main__':
    app.run()