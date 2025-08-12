import jwt
from flask import current_app, session
from .crud import (
    get_chat_list, get_chat_list_empty, get_user_inf, get_name_friend, get_avatar_friend, 
    get_chat_state_id, get_avatar_group, get_base_messages)

def clear_session():
    session.clear()
    session["logged_in"] = False

def get_token(user_id, chat_id):
    payload = {"user": user_id, "chat": chat_id}
    token = jwt.encode(payload, current_app.config["SECRET_KEY"])
    return token.split(".")[1]
 
def session_edit(**kwargs):
    if not kwargs:
        login = session.get("login")
        # print("session_edit login: ", login)
        user_id, username, name, lastname, bday, avatar, bio = get_user_inf(login)  
        # print("session_edit: ", user_id, username, name, lastname, bday, avatar, bio)
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
    
def get_chats():
    user_id = session.get("user_id")
    chat_list = get_chat_list(user_id)
    chat_list_empty = get_chat_list_empty(user_id)
    chats = []
    if chat_list:
        for elem in chat_list:
            chat_id = elem.get('chat_id')
            chat_name = elem.get('chat_name')
            chat_type_id = elem.get('type_id')
            chat_state_id = elem.get('chat_state_id')
            chat_role_id = elem.get('role_id')
            last_msg_elem = [elem.get('message'), elem.get('last_ts')]
            if last_msg_elem != None:
                last_msg, date = last_msg_elem
                date = date.strftime('%d.%m %H:%M')
                # print('date get_chats: ', date)
            else:
                last_msg = ""
                date = ""
            if chat_type_id == 1:
                first_id = int(chat_name.split("_")[0])
                second_id = int(chat_name.split("_")[1])
                friend_id = second_id if user_id == first_id else first_id
                name, lastname = get_name_friend(friend_id)
                chat_avatar = get_avatar_friend(friend_id)
                chat_name = f"{name} {lastname}"
                chat_friend_state_id = get_chat_state_id(chat_id, friend_id)
            elif chat_type_id == 2:
                chat_avatar = get_avatar_group(chat_id)
                chat_friend_state_id = None
            cnt_unread_msg = 100
            chats.append((chat_id, chat_name, chat_type_id, chat_avatar, last_msg, date, cnt_unread_msg, chat_state_id, chat_friend_state_id, chat_role_id))
    
    if chat_list_empty:
        for elem in chat_list_empty:
            chat_id = elem.get('chat_id')
            chat_name = elem.get('chat_name')
            chat_type_id = elem.get('type_id')
            chat_state_id = elem.get('chat_state_id')
            chat_role_id = elem.get('role_id')
            last_msg = ''
            date = ''
            if chat_type_id == 1:
                first_id = int(chat_name.split("_")[0])
                second_id = int(chat_name.split("_")[1])
                friend_id = second_id if user_id == first_id else first_id
                name, lastname = get_name_friend(friend_id)
                chat_avatar = get_avatar_friend(friend_id)
                chat_name = f"{name} {lastname}"
                chat_friend_state_id = get_chat_state_id(chat_id, friend_id)
            elif chat_type_id == 2:
                chat_avatar = get_avatar_group(chat_id)
                chat_friend_state_id = None
            cnt_unread_msg = 100
            chats.append((chat_id, chat_name, chat_type_id, chat_avatar, last_msg, date, cnt_unread_msg, chat_state_id, chat_friend_state_id, chat_role_id))
    return chats if chats else None

def get_messages(chat_id):
    messages = get_base_messages(chat_id)
    # print('get messages: ', messages)
    displayed_messages = {}
    if messages:
        for msg in messages:
            if displayed_messages.get(msg.get('timestamp').strftime('%d.%m.%Y')):
                displayed_messages[msg.get('timestamp').strftime('%d.%m.%Y')].append({"message_id" : msg.get('id'), "message" : msg.get('message'), "message_type_id" : msg.get('type_id'), "timestamp" : msg.get('timestamp').strftime('%H:%M'), "user_id" : msg.get('user_id'), "chat_id" : msg.get('chat_id'), "state_id" : msg.get('state_id'), "content_state_id" : msg.get('content_state_id'), "type_chat" : msg.get('type_chat'), "avatar" : msg.get('avatar'), "username" : msg.get('username')})
            else:
                displayed_messages[msg.get('timestamp').strftime('%d.%m.%Y')] = [{"message_id" : msg.get('id'), "message" : msg.get('message'), "message_type_id" : msg.get('type_id'), "timestamp" : msg.get('timestamp').strftime('%H:%M'), "user_id" : msg.get('user_id'), "chat_id" : msg.get('chat_id'), "state_id" : msg.get('state_id'), "content_state_id" : msg.get('content_state_id'), "type_chat" : msg.get('type_chat'), "avatar" : msg.get('avatar'), "username" : msg.get('username')}]
        # print('Messages: ', displayed_messages)
        return displayed_messages
    else: return None
