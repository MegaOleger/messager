from flask import Flask, render_template, request, abort, session, redirect
from datetime import datetime
import jwt
from dateutil import parser
from flask_socketio import SocketIO, emit
import sqlconnector as sql
import logging 

logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.secret_key = "test"
socketIO = SocketIO(app)

def get_token(user_id, chat_id):
    payload = {
        'user' : user_id,
        'chat' : chat_id
    }
    token = jwt.encode(payload=payload, key=app.secret_key) 
    token = token.split('.')[1]
    return token

def get_chats():
    user_id = session.get("user_id")
    chat_list = sql.get_chat_list(user_id)
    chat_list_empty = sql.get_chat_list_empty(user_id)
    # print('chat_list get_chats: ', chat_list)
    # print('chat_list_empty: ', chat_list_empty)
    chats = []
    if chat_list:
        for elem in chat_list:
            chat_id = elem[0]
            chat_name = elem[1]
            chat_type_id = elem[2]
            chat_state_id = elem[3]
            chat_role_id = elem[4]
            last_msg_elem = [elem[5], elem[6]]
            if last_msg_elem != None:
                last_msg, date = last_msg_elem
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m %H:%M')
            else:
                last_msg = ""
                date = ""
            if chat_type_id == 1:
                first_id = int(chat_name.split("_")[0])
                second_id = int(chat_name.split("_")[1])
                friend_id = second_id if user_id == first_id else first_id
                name, lastname = sql.get_name_friend(friend_id)
                chat_avatar = sql.get_avatar_friend(friend_id)
                chat_name = f"{name} {lastname}"
                chat_friend_state_id = sql.get_chat_state_id(elem[0], friend_id)
            elif chat_type_id == 2:
                chat_avatar = sql.get_avatar_group(elem[0])
                chat_friend_state_id = None
            cnt_unread_msg = 100
            chats.append((elem[0], chat_name, chat_type_id, chat_avatar, last_msg, date, cnt_unread_msg, chat_state_id, chat_friend_state_id, chat_role_id))
    
    if chat_list_empty:
        for elem in chat_list_empty:
            chat_id = elem[0]
            chat_name = elem[1]
            chat_type_id = elem[2]
            chat_state_id = elem[3]
            chat_role_id = elem[4]
            last_msg = ''
            date = ''
            if chat_type_id == 1:
                first_id = int(chat_name.split("_")[0])
                second_id = int(chat_name.split("_")[1])
                friend_id = second_id if user_id == first_id else first_id
                name, lastname = sql.get_name_friend(friend_id)
                chat_avatar = sql.get_avatar_friend(friend_id)
                chat_name = f"{name} {lastname}"
                chat_friend_state_id = sql.get_chat_state_id(chat_id, friend_id)
            elif chat_type_id == 2:
                chat_avatar = sql.get_avatar_group(chat_id)
                chat_friend_state_id = None
            cnt_unread_msg = 100
            chats.append((chat_id, chat_name, chat_type_id, chat_avatar, last_msg, date, cnt_unread_msg, chat_state_id, chat_friend_state_id, chat_role_id))
    # print("chats: ", chats)
    return chats if chats else None


@app.route("/")
def index():
    if session.get("logged_in"):
        session_edit()
        return redirect("/home")
    else:
        session["logged_in"] = False
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        logger.info("post on /login")
        input_login = request.form["user_login"]
        input_password = request.form["password"]
        valid_password = sql.get_password(input_login)
        if valid_password is None:
            logger.error(f"user {input_login} not found")
            message_login = f"{input_login} is not registered"
            error_login = True
            return render_template('login.html', message_login=message_login, input_login=input_login, input_password=input_password, error_login=error_login)

        elif valid_password == input_password:
            session["logged_in"] = True
            session['login'] = input_login
            session_edit()
            return redirect("/home")
        else:
            message_password = "The password is incorrect"
            error_password = True
            return render_template('login.html', message_password=message_password, input_login=input_login, input_password=input_password, error_password=error_password)
    else:
        return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method=="POST":
        input_login = request.form['reg_login']
        input_password = request.form['reg_password']
        input_name = request.form['reg_name']
        input_lastname = request.form['reg_lastname']
        input_bday = request.form['bday']
        user_id = sql.check_login(input_login)

        if user_id is not None:
            message_login = f"{input_login} is already occupied"
            error_reg = True
            return render_template('registration.html', message_login=message_login, input_login=input_login, input_password=input_password, input_name=input_name, input_lastname=input_lastname, input_bday=input_bday, error_reg=error_reg)
        else:
            avatar = "default_avatar.jpg"
            bio = "Bio is empty"
            sql.create_user(input_login, input_name, input_lastname, input_bday, input_password, avatar, bio)
            session["logged_in"] = True
            session['login'] = input_login
            session_edit()
            return redirect("/home")
    else:
        return render_template('registration.html')

def clear_session():
    session.clear()
    session["logged_in"] = False

@app.route("/logout")
def logout():
    clear_session()
    return redirect("/")

@app.route("/home", methods=["GET", "POST"])
def home():
    if session.get("logged_in"):
        upd_chat_list()
        upd_chat_header()
        upd_chat_messages()
        upd_chat_state()
        print(f"CHAT_STATE_ID: {session.get('chat_state_id')}")
        return render_template("home.html")
    else:
        return redirect("/")

@app.route("/settings", methods=["GET"])
def settings():
    if session.get("logged_in"):
        username, name, lastname, bday, avatar, bio = get_session(session.get("login"))
        # print(username)
        if avatar is None:
            avatar = "default_avatar.jpg"
        return render_template("settings.html", username=username, name=name, lastname=lastname, bday=bday, avatar=avatar, bio=bio)
    else:
        return redirect("/")

@app.route("/delete_user")
def delete_user():
    if session.get("logged_in"):
        if sql.delete_user(session.get("login"), session.get("user_id")):
            return redirect("/logout")
        else:
            return False
    else:
        return redirect("/")
    
@app.route("/edit_profile", methods=["GET"])
def edit_profile():
    if session.get("logged_in"):
        username, name, lastname, bday, avatar, bio = get_session(session.get("login"))
        return render_template("edit.html", username=username, name=name, lastname=lastname, bday=bday, avatar=avatar, bio=bio)
    else:
        return redirect("/")

@app.route("/save_edit", methods=["POST", "GET"])
def save_edit():
    if request.method=="POST":
        if session.get("logged_in"):
            
            input_name = request.form['input_name']
            input_lastname = request.form['input_lastname']
            input_username = request.form['input_username']
            input_bday = request.form['input_bday']
            input_bio = request.form['input_bio']
            input_avatar = request.files['input_avatar']

            name = input_name if input_name else session.get('name')
            lastname = input_lastname if input_lastname else session.get('lastname')
            username = input_username if input_username else session.get('username')
            bday = input_bday if input_bday else session.get('bday')
            avatar = input_avatar if input_avatar else session.get('avatar')
            bio = input_bio if input_bio else session.get('bio')
            

            if avatar and type(avatar) is not str and avatar.filename:
                filename = f"{username}.{avatar.filename.split('.')[-1]}"
                avatar.save(f"static\\images\\avatars\\{filename}")
            else: 
                filename = avatar

            sql.edit_profile(session.get("login"), filename, name, lastname, username, bday, bio)
            session_edit(name=name, lastname=lastname, username=username, bday=bday, bio=bio, avatar=filename)
            return redirect("/edit_profile")
        else: 
            return redirect("/")
    else:
        return redirect('/edit_profile')

@app.route("/reset_edit")
def reset_edit():
    if session.get("logged_in"):
        return redirect("/edit_profile")
    else: 
        return redirect("/")
        
def session_edit(**kwargs):
    if not kwargs:
        login = session.get("login")
        print("SESSION: ", sql.select_info(login))
        username, name, lastname, bday, avatar, bio, user_id = sql.select_info(login)
        if avatar is None:
            avatar = "default_avatar.jpg"
        if username is None:
            username = login
        if bio is None:
            bio = "Bio is empty"
        session['username'] = username
        session['name'] = name
        session['lastname'] = lastname
        session['bday'] = bday
        session['avatar'] = avatar
        session['bio'] = bio
        session['user_id'] = user_id
    
    else:
        session['username'] = kwargs.get("username")
        session['name'] = kwargs.get("name")
        session['lastname'] = kwargs.get("lastname")
        session['bday'] = kwargs.get("bday")
        session['avatar'] = kwargs.get("avatar")
        session['bio'] = kwargs.get("bio")

def get_session(login):
    if session.get('login') == login:
        return session.get('username'), session.get('name'), session.get('lastname'), session.get('bday'), session.get('avatar'), session.get('bio')

@app.route("/create_chat", methods=["POST", 'GET'])
def create_chat():
    if request.method=="POST":
        friend_username = request.form['friend_username']
        username = session.get('username')
        if friend_username != username: 
            if friend_username[0] == "@":
                friend_username = friend_username[1:]
            if sql.check_username(friend_username) is not None:
                user_id = session.get('user_id')
                friend_id = sql.check_username(friend_username)
                if sql.check_chat_name(f"{user_id}_{friend_id}", f"{friend_id}_{user_id}") is None:
                    chat_name = f"{user_id}_{friend_id}"
                    # print('chat_name: ', type(chat_name))
                    # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    chat_type_id = 1
                    role_id = 1
                    chat_state_id = 1
                    # print("create_chat: ", user_id, chat_name, chat_type_id, role_id, chat_state_id)
                    chat_id = session['chat_id'] = sql.create_chat(user_id, chat_name, chat_type_id, role_id, chat_state_id)
                    # token = get_token(user_id, chat_id)
                    # sql.add_token_chat(chat_id, token)
                    sql.add_members(chat_id, friend_id)
                    return redirect('/home')
                else:
                    msg = 'Such a chat has already been created'
                    return redirect("/home")
            else:
                msg = 'There is no such username'
                return redirect("/home")
        else:
            msg = 'This is your username'
            return redirect("/home")

@app.route("/join_group", methods=['POST', 'GET'])
def join_group():
    if request.method=="POST":
        token = request.form['code_to_join']
        if sql.check_code(token) is not None:
            user_id = session.get('user_id')
            chat_id = sql.get_chat_id(token)
            if not sql.check_group_joined(user_id, chat_id):
                role_id = 3
                sql.join_group(chat_id, user_id, role_id)
                return redirect('/home')
            else:
                msg = 'You have already joined'
                return render_template('home.html', message_join=msg)

        else:
            msg = 'The code was not found'
            return render_template('home.html', message_join=msg)

@app.route("/create_group", methods=['POST', 'GET'])
def create_group():
    if request.method=="POST":
        chat_name = request.form['name_group']
        # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = session.get('user_id')
        type_chat = 2
        role_id = 1
        chat_state_id = 1
        avatar = "default_group.png"
        chat_id = sql.create_chat(user_id, chat_name, type_chat, role_id, chat_state_id)
        open_chat(chat_id)
        sql.add_avatar_chat(chat_id, avatar)
        token = get_token(user_id, chat_id)
        sql.add_token_chat(chat_id, token)
        # return render_template('home.html', code = token)
        return redirect('/home')

@app.route("/open_chat/<int:chat_id>", methods=['POST', 'GET'])
def open_chat(chat_id):
    user_id = session.get('user_id')
    chat_name = sql.get_chat_inf("name", chat_id)
    chat_type_id = sql.get_chat_inf("type", chat_id)
    chat_state_id = sql.get_chat_state_id(chat_id, user_id)
    chat_role_id = sql.get_role_id(chat_id, user_id)
    if chat_type_id == 1: #personal chat
        first_id = int(chat_name.split("_")[0])
        second_id = int(chat_name.split("_")[1])
        friend_id = second_id if user_id == first_id else first_id
        name, lastname = sql.get_name_friend(friend_id)
        chat_avatar = sql.get_avatar_friend(friend_id)
        chat_name = f"{name} {lastname}"
        session['friend_id'] = friend_id
        chat_friend_state_id = sql.get_chat_state_id(chat_id, friend_id)
    elif chat_type_id == 2: #group chat 
        chat_avatar = sql.get_avatar_group(chat_id)
        chat_friend_state_id = None
        session['friend_id'] = None
    session['chat_id'] = chat_id
    session['chat_name'] = chat_name
    session['chat_type_id'] = chat_type_id
    session['chat_avatar'] = chat_avatar
    session['chat_state_id'] = chat_state_id
    session['chat_friend_state_id'] = chat_friend_state_id
    session['chat_role_id'] = chat_role_id
    return redirect("/home")

@app.route("/message", methods=["POST", 'GET'])
def message():
    if request.method == 'POST':
        # print(f"OPEN CHAT; \nchat_friend_state_id: {session.get('chat_friend_state_id')} \nchat_state_id: {session.get('chat_state_id')}")
        if session.get('chat_friend_state_id') == 1 and session.get('chat_state_id') == 1 or session.get('chat_type_id'): #if chat is not blocked
            chat_id = session.get('chat_id')
            user_id = session.get("user_id")
            msg = request.form['message']
            type_id = 1 #text
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            state_id = 1
            content_state_id = 1
            member_id = sql.get_member_id(chat_id, user_id)
            sql.save_message(msg, type_id, timestamp, member_id, chat_id, state_id, content_state_id)
            # payload = {'chat_id': chat_id, 'message': msg, 'timestamp': timestamp, 'user_id': user_id}
            socketIO.emit('new_message', msg)
            return redirect("/home")
        else:
            print("The chat is blocked")
            return redirect("/home")
    
@socketIO.on('message')
def handle_websocket_message(data):
    # print("DATA websocket: ", data)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print('TIMESTAMP: ', timestamp)
    chat_id = session.get('chat_id')
    user_id = session.get('user_id')
    payload = {'chat_id': chat_id, 'message': data, 'timestamp': timestamp, 'user_id': user_id}
    # print("payload", payload)
    emit('new_message', payload)

@socketIO.on('chat_action')
def handle_websocket_chat_action():
    emit('chat_action')

def get_messages(chat_id):
    messages = sql.get_messages(chat_id)
    # print("Messages: ", messages, type(messages))
    displayed_messages = []
    if messages:
        for msg in messages:
            displayed_messages.append({"message_id" : msg[0], "message" : msg[1], "message_type_id" : msg[2], "timestamp" : datetime.strptime(msg[3], '%Y-%m-%d %H:%M:%S').strftime('%H:%M'), "user_id" : msg[4], "chat_id" : msg[5], "state_id" : msg[6], "content_state_id" : msg[7], "owner" : True if msg[4]==session.get("user_id") else False, "type_chat" : msg[8], "avatar" : msg[9]})
        # print(displayed_messages)
        return displayed_messages
    else: return None

@app.route("/block_user")
def block_user():
    friend_id = session.get('friend_id')
    sql.block_user(session.get('chat_id'), friend_id)
    session['chat_friend_state_id'] = 2
    socketIO.emit('chat_action')
    return redirect("/home")

@app.route("/unblock_user")
def unblock_user():
    friend_id = session.get('friend_id')
    sql.unblock_user(session.get('chat_id'), friend_id)
    session['chat_friend_state_id'] = 1
    socketIO.emit('chat_action')
    return redirect("/home")

@app.route("/leave_chat")
def leave_chat():
    sql.leave_chat(session.get('chat_id'), session.get('user_id'))
    session['chat_id'] = None
    socketIO.emit('chat_action')
    return redirect("/home")

@app.route("/clear_chat")
def clear_chat():
    sql.clear_chat(session.get('chat_id'))
    socketIO.emit('chat_action')
    return redirect("/home")

@app.route("/delete_chat")
def delete_chat():
    chat_id = session.get('chat_id')
    user_id = session.get('user_id')
    sql.leave_chat(chat_id, user_id)
    # get all members before delete
    all_members_id = sql.get_all_members_id(chat_id)
    for member_id in all_members_id:
        sql.leave_chat(chat_id, member_id)
    sql.delete_chat(chat_id)
    session['chat_id'] = None
    socketIO.emit('chat_action')
    return redirect("/home")

@app.route("/upd_chat_state")
def upd_chat_state():
    chat_state_id = sql.get_chat_state_id(session.get('chat_id'), session.get('user_id'))
    session['chat_state_id'] = chat_state_id


@app.route("/upd_chat_list")
def upd_chat_list():
    chat_id = session.get('chat_id')
    chats = get_chats()
    # print("CHATS list: ", chats)
    if chat_id:
        chat_name = session.get('chat_name')
        chat_type_id = session.get('chat_type_id')
        chat_avatar = session.get('chat_avatar')
        chat_state_id = session.get('chat_state_id')
        chat_friend_state_id = session.get('chat_friend_state_id')
        # print(f"IF chat_id \nchat_friend_state_id: {chat_friend_state_id} \nchat_state_id: {chat_state_id} \nName: {session.get('name')}")
        chat_role_id = session.get('chat_role_id')
        if chat_type_id == 2:
            cnt_members = sql.cnt_members(chat_id)
        else:
            cnt_members = None
        chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, cnt_members, chat_state_id, chat_friend_state_id, chat_role_id]
        # print("chat_inf: ", chat_inf) 
        return render_template("chat_list.html", chat_list=chats, chat=chat_inf)
    else:
        if chats:
            chat_inf = chats[0]
            # print("CHAT_INF chat_list: ", chat_inf)
            chat_id = session['chat_id'] = chat_inf[0]
            chat_name = session['chat_name'] = chat_inf[1]
            chat_type_id = session['chat_type_id'] = chat_inf[2]
            chat_avatar = session['chat_avatar'] = chat_inf[3]
            chat_state_id = session['chat_state_id'] = chat_inf[7]
            chat_friend_state_id = session['chat_friend_state_id'] = chat_inf[8]
            print('IF NOT chat_id chat_friend_state_id: ', chat_friend_state_id)
            chat_role_id = session['chat_role_id'] = chat_inf[9]
            # print("Role_id: ", chat_role_id)
            if chat_type_id == 2:
                cnt_members = sql.cnt_members(chat_id)
            else:
                cnt_members = None
            chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, cnt_members, chat_state_id, chat_friend_state_id, chat_role_id]
            # print("chat_inf: ", chat_inf)
            return render_template("chat_list.html", chat_list=chats, chat=chat_inf)
        else:
            return render_template("chat_list.html", chat=None)

@app.route("/upd_chat_messages")
def upd_chat_messages():
    chat_id = session.get('chat_id')
    chats = get_chats()
    # print("CHATS messages: ", chats)
    if chat_id:
        chat_name = session.get('chat_name')
        chat_type_id = session.get('chat_type_id')
        chat_avatar = session.get('chat_avatar')
        chat_state_id = session.get('chat_state_id')
        chat_friend_state_id = session.get('chat_friend_state_id')
        chat_role_id = session.get('chat_role_id')
        cnt_members = 0
        chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, cnt_members, chat_state_id, chat_friend_state_id, chat_role_id]
        # print("chat_inf messages: ", chat_inf)
        messages = get_messages(chat_id)
        if messages:
            return render_template("chat_messages.html", chat=chat_inf, messages=messages)
        else:
            return render_template("chat_messages.html", chat=chat_inf)
    else:
        if chats:
            chat_inf = chats[0]
            # print("CHAT_INF: ", chat_inf)
            chat_id = session['chat_id'] = chat_inf[0]
            chat_name = session['chat_name'] = chat_inf[1]
            chat_type_id = session['chat_type_id'] = chat_inf[2]
            chat_avatar = session['chat_avatar'] = chat_inf[3]
            chat_state_id = session['chat_state_id'] = chat_inf[7]
            chat_friend_state_id = session['chat_friend_state_id'] = chat_inf[8]
            chat_role_id = session['chat_role_id'] = chat_inf[9]
            chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, chat_state_id, chat_friend_state_id, chat_role_id]
            # print("chat_inf: ", chat_inf)
            messages = get_messages(chat_id)
            if messages:
                return render_template("chat_messages.html", chat=chat_inf, messages=messages)
            else:
                return render_template("chat_messages.html", chat=chat_inf)
        else:
            return render_template("chat_messages.html", chat=None)

@app.route('/upd_chat_header')
def upd_chat_header():
    chat_id = session.get('chat_id')
    chats = get_chats()
    # print("CHATS: ", chats)
    if chat_id:
        chat_name = session.get('chat_name')
        chat_type_id = session.get('chat_type_id')
        chat_avatar = session.get('chat_avatar')
        chat_state_id = session.get('chat_state_id')
        chat_friend_state_id = session.get('chat_friend_state_id')
        chat_role_id = session.get('chat_role_id')
        if chat_type_id == 2:
            cnt_members = sql.cnt_members(chat_id)
        else:
            cnt_members = None
        chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, cnt_members, chat_state_id, chat_friend_state_id, chat_role_id]
        return render_template("chat_header.html", chat_list=chats, chat=chat_inf)
    else:
        if chats:
            chat_inf = chats[0]
            # print("CHAT_INF: ", chat_inf)
            chat_id = session['chat_id'] = chat_inf[0]
            chat_name = session['chat_name'] = chat_inf[1]
            chat_type_id = session['chat_type_id'] = chat_inf[2]
            chat_avatar = session['chat_avatar'] = chat_inf[3]
            chat_state_id = session['chat_state_id'] = chat_inf[7]
            chat_friend_state_id = session['chat_friend_state_id'] = chat_inf[8]
            chat_role_id = session['chat_role_id'] = chat_inf[9]
            chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, chat_state_id, chat_friend_state_id, chat_role_id]
            # print("chat_inf: ", chat_inf)
            return render_template("chat_header.html", chat=chat_inf)
        else:
            return render_template("chat_header.html", chat=None)

@app.route('/copy_inv_code')
def copy_inf_code():
    token = sql.get_chat_inf('token', session.get('chat_id'))
    if token:
        return token
    else:
        return redirect("/home")

@app.route('/upd_members_list')
def upd_members_list(chat_id):
    members = sql.get_members(chat_id)
    render_template('members_list', members=members)

@app.route('/chat_preview')
def chat_preview():
    chat_id = session.get('chat_id')
    chat_name = session.get('chat_name')
    cnt_members = session.get('cnt_members')
    type_chat = session.get('type_chat')
    upd_members_list(chat_id)
    render_template('chat_preview.html', chat_name=chat_name, cnt_members=cnt_members, type_chat=type_chat)

if __name__ == "__main__":
    socketIO.run(app, debug=True)