from flask import session, redirect, request, render_template, Blueprint
import logging 
# import __init__
from datetime import datetime

logger = logging.Logger(__name__)
main_bp = Blueprint("main", __name__)

from .crud import (
    create_user, check_login, get_password,
    edit_profile, delete_user, create_chat, save_message,
    get_chat_inf, db_join_group, db_leave_chat, db_block_user,
    db_unblock_user, db_clear_chat, get_members, 
    get_member_id, get_avatar_group, get_chat_state_id, get_role_id,
    check_chat_name, check_group_joined, check_code, get_name_friend,
    add_avatar_chat, check_username, add_members, get_chat_id, add_token_chat, 
    get_avatar_friend, get_cnt_members, get_chat_id_by_names, get_user_info_by_id, 
    delete_message, edit_message, forward_message, reply_message, get_user_id_by_username
)

from .utils import (session_edit, clear_session, get_session, get_chats, get_token, get_messages)
from .extensions import socketio

@main_bp.route("/")
def index():
    if session.get("logged_in"):
        session_edit()
        return redirect("/home")
    else:
        session["logged_in"] = False
        return redirect("/login")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        logger.info("post on /login")
        input_login = request.form["user_login"]
        input_password = request.form["password"]
        valid_password = get_password(input_login)
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

@main_bp.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method=="POST":
        input_login = request.form['reg_login']
        input_password = request.form['reg_password']
        input_name = request.form['reg_name']
        input_lastname = request.form['reg_lastname']
        input_bday = request.form['bday']
        user_id = check_login(input_login)

        if user_id is not None:
            message_login = f"{input_login} is already occupied"
            error_reg = True
            return render_template('registration.html', message_login=message_login, input_login=input_login, input_password=input_password, input_name=input_name, input_lastname=input_lastname, input_bday=input_bday, error_reg=error_reg)
        else:
            avatar = "default_avatar.jpg"
            bio = "Bio is empty"
            create_user(input_login, input_name, input_lastname, input_bday, input_password, avatar, bio)
            session["logged_in"] = True
            session['login'] = input_login
            session_edit()
            return redirect("/home")
    else:
        return render_template('registration.html')
    
@main_bp.route("/logout")
def logout():
    clear_session()
    return redirect("/")

@main_bp.route("/home", methods=["GET", "POST"])
def home():
    if session.get("logged_in"):
        upd_chat_list()
        upd_chat_header()
        upd_chat_messages()
        return render_template("home.html")
    else:
        return redirect("/")

@main_bp.route("/settings", methods=["GET"])
def settings():
    if session.get("logged_in"):
        username, name, lastname, bday, avatar, bio = get_session(session.get("login"))
        print(username, name, lastname, bday, avatar, bio)
        if avatar is None:
            avatar = "default_avatar.jpg"
        return render_template("settings.html", 
                               username=username, 
                               name=name, 
                               lastname=lastname, 
                               bday=bday, 
                               avatar=avatar, 
                               bio=bio)
    else:
        return redirect("/")

@main_bp.route("/delete_user")
def delete_user():
    if session.get("logged_in"):
        if delete_user(session.get("login"), session.get("user_id")):
            return redirect("/logout")
        else:
            return False
    else:
        return redirect("/")
    
@main_bp.route("/edit_profile", methods=["GET"])
def edit_profile():
    if session.get("logged_in"):
        username, name, lastname, bday, avatar, bio = get_session(session.get("login"))
        return render_template("edit.html", username=username, name=name, lastname=lastname, bday=bday, avatar=avatar, bio=bio)
    else:
        return redirect("/")

@main_bp.route("/save_edit", methods=["POST", "GET"])
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

            edit_profile(session.get("login"), filename, name, lastname, username, bday, bio)
            session_edit(name=name, lastname=lastname, username=username, bday=bday, bio=bio, avatar=filename)
            return redirect("/edit_profile")
        else: 
            return redirect("/")
    else:
        return redirect('/edit_profile')

@main_bp.route("/reset_edit")
def reset_edit():
    if session.get("logged_in"):
        return redirect("/edit_profile")
    else: 
        return redirect("/")
    
@main_bp.route("/create_chat", methods=["POST", 'GET'])
def create_chat():
    if request.method=="POST":
        friend_username = request.form['friend_username']
        username = session.get('username')
        if friend_username != username: 
            if friend_username[0] == "@":
                friend_username = friend_username[1:]
            if check_username(friend_username) is not None:
                user_id = session.get('user_id')
                friend_id = check_username(friend_username)
                if check_chat_name(f"{user_id}_{friend_id}", f"{friend_id}_{user_id}") is None:
                    chat_name = f"{user_id}_{friend_id}"
                    # print('chat_name: ', type(chat_name))
                    # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    chat_type_id = 1
                    role_id = 1
                    chat_state_id = 1
                    # print("create_chat: ", user_id, chat_name, chat_type_id, role_id, chat_state_id)
                    chat_id = session['chat_id'] = create_chat(user_id, chat_name, chat_type_id, role_id, chat_state_id)
                    # token = get_token(user_id, chat_id)
                    # sql.add_token_chat(chat_id, token)
                    add_members(chat_id, friend_id)
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

@main_bp.route("/join_group", methods=['POST', 'GET'])
def join_group():
    if request.method=="POST":
        token = request.form['code_to_join']
        if check_code(token) is not None:
            user_id = session.get('user_id')
            chat_id = get_chat_id(token)
            if not check_group_joined(chat_id, user_id):
                role_id = 3
                db_join_group(chat_id, user_id, role_id)
                return redirect('/home')
            else:
                msg = 'You have already joined'
                return render_template('home.html', message_join=msg)

        else:
            msg = 'The code was not found'
            return render_template('home.html', message_join=msg)

@main_bp.route("/create_group", methods=['POST', 'GET'])
def create_group():
    if request.method=="POST":
        chat_name = request.form['name_group']
        # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = session.get('user_id')
        type_chat = 2
        role_id = 1
        chat_state_id = 1
        avatar = "default_group.png"
        chat_id = create_chat(user_id, chat_name, type_chat, role_id, chat_state_id)
        open_chat(chat_id)
        add_avatar_chat(chat_id, avatar)
        token = get_token(user_id, chat_id)
        add_token_chat(chat_id, token)
        # return render_template('home.html', code = token)
        return redirect('/home')

@main_bp.route("/open_chat/<int:chat_id>", methods=['POST', 'GET'])
def open_chat(chat_id):
    user_id = session.get('user_id')
    chat_name = get_chat_inf("name", chat_id)
    chat_type_id = get_chat_inf("type", chat_id)
    chat_state_id = get_chat_state_id(chat_id, user_id)
    chat_role_id = get_role_id(chat_id, user_id)
    if chat_type_id == 1:
        first_id = int(chat_name.split("_")[0])
        second_id = int(chat_name.split("_")[1])
        friend_id = second_id if user_id == first_id else first_id
        name, lastname = get_name_friend(friend_id)
        chat_avatar = get_avatar_friend(friend_id)
        chat_name = f"{name} {lastname}"
        session['friend_id'] = friend_id
        chat_friend_state_id = get_chat_state_id(chat_id, friend_id)
    elif chat_type_id == 2:
        chat_avatar = get_avatar_group(chat_id)
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

@main_bp.route("/message", methods=["POST", 'GET'])
def message():
    if request.method == 'POST':
        # msg = request.form['message']
        data = request.get_json() 
        # print("data: ", data)
        msg = data.get("msg") 
        reply_id = data.get("reply_id")
        # print("msg: ", msg, "reply_id: ", reply_id)

        type_id = 1 #text
        timestamp = datetime.now()
        user_id = session.get("user_id")
        chat_id = session.get('chat_id')
        state_id = 1
        content_state_id = 1
        member_id = get_member_id(chat_id, user_id)
        msg_id = save_message(msg, type_id, timestamp, member_id, chat_id, state_id, content_state_id)
        if reply_id:
            reply_message(msg_id, reply_id)
        
        # payload = {'chat_id': chat_id, 'message': msg, 'timestamp': timestamp, 'user_id': user_id}
        socketio.emit('new_message', msg)
        return redirect("/home")
    

@main_bp.route("/edit_msg", methods=["POST"])
def edit_msg():
    data = request.get_json() 
    # print("data: ", data)
    msg_id = data.get("id") 
    msg_txt = data.get("text")
    # print("msg_id: ", msg_id, "msg_txt: ", msg_txt)
    edit_message(msg_id, msg_txt)
    socketio.emit('edit_message')
    return redirect("/")

@main_bp.route("/forward_msg", methods=["POST"])
def forward_msg():
    data = request.get_json()
    # print("DATA: ", data)
    target_chat_id = data.get('target_chat_id')
    orig_sender = data.get('orig_sender')
    # print('orig_sender: ', orig_sender)
    msg = data.get('msg')
    # print('msg: ', msg)
    type_id = 1 #text
    timestamp = datetime.now()
    user_id = session.get("user_id")
    member_id = get_member_id(target_chat_id, user_id)
    # print("member_id: ", member_id)
    msg_id = save_message(msg, type_id, timestamp, member_id, target_chat_id, 1, 1)
    forward_message(msg_id, orig_sender)
    socketio.emit('new_message', msg)
    return redirect("/")


@main_bp.route("/delete_msg/<int:msg_id>")    
def delete_msg(msg_id):
    delete_message(msg_id)
    socketio.emit('chat_action')
    return redirect("/")

@main_bp.route("/block_user")
def block_user():
    friend_id = session.get('friend_id')
    db_block_user(session.get('chat_id'), friend_id)
    session['chat_friend_state_id'] = 2
    socketio.emit('chat_action')
    return redirect("/home")

@main_bp.route("/unblock_user")
def unblock_user():
    friend_id = session.get('friend_id')
    db_unblock_user(session.get('chat_id'), friend_id)
    session['chat_friend_state_id'] = 1
    socketio.emit('chat_action')
    return redirect("/home")

@main_bp.route("/leave_chat")
def leave_chat():
    db_leave_chat(session.get('chat_id'), session.get('user_id'))
    session['chat_id'] = None
    socketio.emit('chat_action')
    return redirect("/home")

@main_bp.route("/clear_chat")
def clear_chat():
    db_clear_chat(session.get('chat_id'))
    socketio.emit('chat_action')
    return redirect("/home")

@main_bp.route("/delete_chat")
def delete_chat():
    chat_id = session.get('chat_id')
    user_id = session.get('user_id')
    leave_chat(chat_id, user_id)
    delete_chat(chat_id)
    session['chat_id'] = None
    socketio.emit('chat_action')    
    return redirect("/home")

@main_bp.route("/upd_chat_list")
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
        chat_role_id = session.get('chat_role_id')
        if chat_type_id == 2:
            cnt_members = get_cnt_members(chat_id)
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
            chat_role_id = session['chat_role_id'] = chat_inf[9]
            # print("Role_id: ", chat_role_id)
            if chat_type_id == 2:
                cnt_members = get_cnt_members(chat_id)
            else:
                cnt_members = None
            chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, cnt_members, chat_state_id, chat_friend_state_id, chat_role_id]
            # print("chat_inf: ", chat_inf)
            return render_template("chat_list.html", chat_list=chats, chat=chat_inf)
        else:
            return render_template("chat_list.html", chat=None)
        
        
@main_bp.route("/upd_chat_list_forward")
def upd_chat_list_forward():
    chat_id = session.get('chat_id')
    chats = get_chats()
    # print("CHATS list: ", chats)
    if chat_id:
        chat_name = session.get('chat_name')
        chat_type_id = session.get('chat_type_id')
        chat_avatar = session.get('chat_avatar')
        chat_state_id = session.get('chat_state_id')
        chat_friend_state_id = session.get('chat_friend_state_id')
        chat_role_id = session.get('chat_role_id')
        if chat_type_id == 2:
            cnt_members = get_cnt_members(chat_id)
        else:
            cnt_members = None
        chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, cnt_members, chat_state_id, chat_friend_state_id, chat_role_id]
        # print("chat_inf: ", chat_inf) 
        return render_template("chat_list_forward.html", chat_list=chats, chat=chat_inf)
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
            chat_role_id = session['chat_role_id'] = chat_inf[9]
            # print("Role_id: ", chat_role_id)
            if chat_type_id == 2:
                cnt_members = get_cnt_members(chat_id)
            else:
                cnt_members = None
            chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, cnt_members, chat_state_id, chat_friend_state_id, chat_role_id]
            # print("chat_inf: ", chat_inf)
            return render_template("chat_list_forward.html", chat_list=chats, chat=chat_inf)
        else:
            return render_template("chat_list_forward.html", chat=None)


@main_bp.route("/upd_chat_messages")
def upd_chat_messages():
    chat_id = session.get('chat_id')
    chats = get_chats()
    user_id = session.get('user_id')
    # print('user_id: ', user_id)
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
        # print('1 messages: ', messages)
        if messages:
            return render_template("chat_messages.html", chat=chat_inf, messages=messages, user_id=user_id)
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
            # print("Role_id: ", chat_role_id)
            chat_inf = [chat_id, chat_name, chat_type_id, chat_avatar, chat_state_id, chat_friend_state_id, chat_role_id]
            # print("chat_inf: ", chat_inf)
            messages = get_messages(chat_id)
            # print('2 messages: ', messages)
            if messages:
                return render_template("chat_messages.html", chat=chat_inf, messages=messages, user_id=user_id)
            else:
                return render_template("chat_messages.html", chat=chat_inf)
        else:
            return render_template("chat_messages.html", chat=None)

@main_bp.route('/upd_chat_header')
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
            cnt_members = get_cnt_members(chat_id)
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

@main_bp.route('/copy_inv_code')
def copy_inf_code():
    token = get_chat_inf('token', session.get('chat_id'))
    if token:
        return token
    else:
        return redirect("/home")


@main_bp.route("/open_forwarded_profile/<string:sender>", methods=['GET'])
def open_forwarded_profile(sender):
    print('SEnder: ', sender)
    try:
        id = get_user_id_by_username(sender)
        if id is None:
            print('ID is None')
            return redirect('/home')
        print("ID: ", id.get('id'))
        return redirect(f"/open_chat_preview/{id.get('id')}")   
    
    except Exception as e:
        print(f"Error in open_forwarded_profile: {e}")
        return redirect("/home")

@main_bp.route("/open_chat_preview/<int:friend_id>", methods=['POST', 'GET'])
def open_chat_preview(friend_id):
    print('friend_id: ', friend_id)
    user_id = session.get('user_id')
    print('user_id: ', user_id)
    if user_id == friend_id:
        print('user_id = friend_id')
        return redirect("/settings")
    else:
        name, lastname = get_name_friend(friend_id)
        print('name, lastname ', name, lastname)
        chat_name_1 = f'{user_id}_{friend_id}'
        chat_name_2 = f'{friend_id}_{user_id}'
        chat_id = get_chat_id_by_names(chat_name_1, chat_name_2)
        print('chat_id: ', chat_id)
    
        if chat_id:
            print('session_edit')
            session['chat_id'] = chat_id
            print('chat_id: ',chat_id)
            session['chat_name'] = f"{name} {lastname}"
            print(f"{name} {lastname}")
            session['role_id'] = get_role_id(chat_id, user_id)
            print('role: ', get_role_id(chat_id, user_id))
            session['chat_friend_state_id'] = get_chat_state_id(chat_id, friend_id)
            print('state_fr: ', get_chat_state_id(chat_id, friend_id))
            session['chat_state_id'] = get_chat_state_id(chat_id, user_id) 
            print('state: ', get_chat_state_id(chat_id, user_id))
            session['chat_type_id'] = 1
            session['chat_avatar'] = get_avatar_friend(friend_id)
            print('avatar: ', get_avatar_friend(friend_id))
            session['friend_id'] = friend_id
            print('friend_id: ', friend_id)
            print('session_edited')
        else:
            session['chat_name'] = f'{name} {lastname}'
            session['chat_type_id'] = 1
            session['role_id'] = 1
            session['chat_state_id'] = 1
            session['chat_friend_state_id'] = 1
            chat_id = create_chat(user_id, f'{user_id}_{friend_id}', 1)
            print('create_chat chat_id: ', chat_id)
            session['chat_id'] = chat_id
            session['friend_id'] = friend_id
            session['chat_avatar'] = get_avatar_friend(friend_id)
            add_members(chat_id, friend_id)
    
        return redirect("/chat_preview")
    

@main_bp.route('/chat_preview')
def chat_preview():
    chat_name = session.get('chat_name')
    chat_type_id = session.get('chat_type_id')
    chat_avatar = session.get('chat_avatar')
    chat_id = session.get('chat_id')
    # print(f'chat_name: {chat_name}\ncnt_members: {cnt_members}\nchat_type_id: {chat_type_id}')
    if chat_type_id == 1:
        friend_id = session.get('friend_id')
        print('! friend_id: ', friend_id)
        role_id = session.get('role_id')
        print('! role_id: ', role_id)
        chat_friend_state_id = session.get('chat_friend_state_id')
        print('! fr state_id: ', chat_friend_state_id)
        friend_info = get_user_info_by_id(friend_id)
        print('! fr info: ', friend_info)
        print('render chat_preview')
        return render_template("chat_preview.html", chat_name=chat_name, chat_type_id=chat_type_id, chat_avatar = chat_avatar, role_id = role_id, chat_friend_state_id = chat_friend_state_id, friend_info=friend_info, chat_id=chat_id)
    elif chat_type_id == 2:
        members = get_members(chat_id)
        # print('members: ', members)
        cnt_members = get_cnt_members(chat_id)
        return render_template("chat_preview.html", 
                            chat_name=chat_name, 
                            cnt_members=cnt_members, 
                            chat_type_id=chat_type_id, 
                            chat_avatar=chat_avatar,
                            members=members,
                            user_id=session.get('user_id'),
                            chat_id=chat_id)
    