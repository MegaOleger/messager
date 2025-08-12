from datetime import datetime
from sqlalchemy import func, or_
from .models import (
    User, Password, Chat, Member, Role, ChatState, ChatType,
    EntryType, MessageContentState, MessageState, MessageEntry
)
from .extensions import db

def get_user_by_login(login: str):
    u = User.query.filter_by(login=login).first()
    user = {
        'id': u.id,
        'username': u.username,
        'name': u.name,
        'lastname': u.lastname,
        'bday': u.bday,
        'avatar': u.avatar,
        'bio': u.bio
    }
    # print('get_user_by_login: ', user)

    return user if u else None

def get_user_inf(login: str):
    u = get_user_by_login(login)
    # print("get_user_inf: ", u)
    # print('Name: ', u.get('name'))
    if not u:
        return None
    user = {
        'id': u['id'],
        'username': u.get('username') or u.get('login'),
        'name': u.get('name'),
        'lastname': u.get('lastname'),
        'bday': u.get('bday'),
        'avatar': u.get('avatar'),
        'bio': u.get('bio')
    }
    # print('get_user_inf: ', u['id'], u.get('username'), u.get('name'), u.get('lastname'), u.get('bday'), u.get('avatar'), u.get('bio'))
    return u['id'], u.get('username'), u.get('name'), u.get('lastname'), u.get('bday'), u.get('avatar'), u.get('bio')

def get_user_info_by_id(user_id: int):
    u = User.query.get(user_id)
    if not u:
        return None
    return {
        'username': u.username,
        'bday': u.bday,
        'bio': u.bio
    }

def create_user(login: str, name: str, lastname: str, bday,
                password_text: str, avatar: str = None, bio: str = None):
    if not all([login, name, lastname, bday, password_text]):
        return None
    user = User(
        login=login,
        name=name,
        lastname=lastname,
        bday=bday,
        avatar=avatar,
        bio=bio
    )
    db.session.add(user)
    db.session.commit()
    pwd = Password(user_id=user.id, password=password_text)
    db.session.add(pwd)
    db.session.commit()
    return user.id

def check_login(login: str):
    u = get_user_by_login(login)
    return u.id if u else None

def check_username(username: str):
    u = User.query.filter_by(username=username).first()
    return u.id if u else None

def get_password(login: str):
    u = User.query.filter_by(login=login).first()
    print('get_password: ', u.passwords)
    if not u or not u.passwords:
        return None
    return u.passwords[0].password

def edit_profile(login: str, avatar: str, name: str,
                 lastname: str, username: str,
                 bday, bio: str):
    u = get_user_by_login(login)
    if not u:
        return False
    u.avatar   = avatar
    u.name     = name
    u.lastname = lastname
    u.username = username
    u.bday     = bday
    u.bio      = bio
    db.session.commit()
    return True

def delete_user(login: str):
    u = get_user_by_login(login)
    if not u:
        return False
    Password.query.filter_by(user_id=u.id).delete()
    User.query.filter_by(id=u.id).delete()
    db.session.commit()
    return True

def create_chat(creator_id: int, chat_name: str, type_id: int,
                role_id: int, chat_state_id: int):
    chat = Chat(
        creator_id=creator_id,
        chat_name=chat_name,
        type_id=type_id
    )
    db.session.add(chat)
    db.session.commit()
    member = Member(
        chat_id=chat.id,
        user_id=creator_id,
        role_id=role_id,
        chat_state_id=chat_state_id
    )
    db.session.add(member)
    db.session.commit()
    return chat.id

def add_avatar_chat(chat_id: int, avatar: str):
    chat = Chat.query.get(chat_id)
    if not chat:
        return False
    chat.avatar = avatar
    db.session.commit()
    return True

def add_token_chat(chat_id: int, token: str):
    chat = Chat.query.get(chat_id)
    if not chat:
        return False
    chat.token = token
    db.session.commit()
    return True

def get_chat_by_token(token: str):
    return Chat.query.filter_by(token=token).first()

def get_chat_inf(target: str, chat_id: int):
    c = Chat.query.get(chat_id)
    if not c:
        return None
    mapping = {
        'name': c.chat_name,
        'creator': c.creator_id,
        'date': c.date_of_creation,
        'token': c.token,
        'type': c.type_id,
        'avatar': c.avatar
    }
    return mapping.get(target)

def join_group(chat_id: int, user_id: int, role_id: int, chat_state_id: int = 1):
    member = Member(
        chat_id=chat_id,
        user_id=user_id,
        role_id=role_id,
        chat_state_id=chat_state_id
    )
    db.session.add(member)
    db.session.commit()
    return True

def leave_chat(chat_id: int, user_id: int):
    Member.query.filter_by(chat_id=chat_id, user_id=user_id).delete()
    db.session.commit()
    return True

def delete_chat(chat_id: int):
    Chat.query.filter_by(id=chat_id).delete()
    db.session.commit()
    return True

def save_message(message: str, type_id: int, timestamp: datetime,
                 member_id: int, chat_id: int,
                 state_id: int, content_state_id: int):
    entry = MessageEntry(
        message=message,
        type_id=type_id,
        timestamp=timestamp,
        member_id=member_id,
        chat_id=chat_id,
        state_id=state_id,
        content_state_id=content_state_id
    )
    db.session.add(entry)
    db.session.commit()
    return entry.id

def delete_message(msg_id: int):
    MessageEntry.query.filter_by(id=msg_id).delete()
    db.session.commit()
    return True

def get_base_messages(chat_id: int):
    rows = db.session.query(
        MessageEntry, Member, User, Chat
    ).join(Member, MessageEntry.member_id == Member.id
    ).join(User, Member.user_id == User.id
    ).join(Chat, MessageEntry.chat_id == Chat.id
    ).filter(MessageEntry.chat_id == chat_id)

    result = []
    for e in rows:
        me = e.MessageEntry
        us = e.User
        ch = e.Chat
        result.append({
            'id': me.id,
            'message': me.message,
            'type_id': me.type_id,
            'timestamp': me.timestamp,
            'user_id': us.id,
            'chat_id': me.chat_id,
            'state_id': me.state_id,
            'content_state_id': me.content_state_id,
            'chat_type_id': ch.type_id,
            'avatar': us.avatar,
            'username': us.username
        })
    return result

def get_chat_list(user_id: int):
    # print('chat_list user_id: ', user_id)
    subq = db.session.query(
        MessageEntry.chat_id,
        func.max(MessageEntry.timestamp).label('last_ts')
    ).group_by(MessageEntry.chat_id).subquery()

    q = db.session.query(
        Member.chat_id,
        Chat.chat_name,
        Chat.type_id,
        Member.chat_state_id,
        Member.role_id,
        MessageEntry.message,
        subq.c.last_ts
    ).join(Chat, Member.chat_id == Chat.id
    ).join(subq, Member.chat_id == subq.c.chat_id
    ).join(MessageEntry,
           (MessageEntry.chat_id == subq.c.chat_id) &
           (MessageEntry.timestamp == subq.c.last_ts)
    ).filter(Member.user_id == user_id
    ).order_by(subq.c.last_ts.desc())

    return [row._asdict() for row in q.all()]

def get_chat_list_empty(user_id: int):
    q = db.session.query(
        Member.chat_id,
        Chat.chat_name,
        Chat.type_id,
        Member.chat_state_id,
        Member.role_id
    ).join(Chat, Member.chat_id == Chat.id
    ).filter(Member.user_id == user_id
    ).outerjoin(MessageEntry, MessageEntry.chat_id == Chat.id
    ).group_by(
        Member.chat_id,
        Chat.chat_name,
        Chat.type_id,
        Member.chat_state_id,
        Member.role_id
    ).having(func.count(MessageEntry.id) == 0)

    return [row._asdict() for row in q.all()]

def get_chat_state_id(chat_id: int, user_id: int):
    m = Member.query.filter_by(chat_id=chat_id, user_id=user_id).first()
    return m.chat_state_id if m else None

def get_role_id(chat_id: int, user_id: int):
    m = Member.query.filter_by(chat_id=chat_id, user_id=user_id).first()
    return m.role_id if m else None

def get_last_msg(chat_id: int):
    m = MessageEntry.query.filter_by(chat_id=chat_id).order_by(MessageEntry.timestamp.desc()).first()
    return {'message': m.message, 'timestamp': m.timestamp} if m else None

def get_cnt_members(chat_id: int):
    return Member.query.filter_by(chat_id=chat_id).count()

def get_members(chat_id: int):
    rows = db.session.query(
        User.id, User.name, User.lastname, User.username, User.avatar
    ).join(Member, Member.user_id == User.id
    ).filter(Member.chat_id == chat_id)

    return [ dict(row._mapping) for row in rows ]

def block_user(chat_id: int, user_id: int):
    m = Member.query.filter_by(chat_id=chat_id, user_id=user_id).first()
    if not m:
        return False
    blocked = ChatState.query.filter_by(state="blocked").first()
    m.chat_state_id = blocked.id if blocked else m.chat_state_id
    db.session.commit()
    return True

def unblock_user(chat_id: int, user_id: int):
    m = Member.query.filter_by(chat_id=chat_id, user_id=user_id).first()
    if not m:
        return False
    active = ChatState.query.filter_by(state="active").first()
    m.chat_state_id = active.id if active else m.chat_state_id
    db.session.commit()
    return True

def clear_chat(chat_id: int):
    MessageEntry.query.filter_by(chat_id=chat_id).delete()
    db.session.commit()
    return True

def get_chat_id_by_names(name1: str, name2: str):
    c = Chat.query.filter(or_(Chat.chat_name == name1, Chat.chat_name == name2)).first()
    return c.id if c else None
 
def get_member_id(chat_id: int, user_id: int):
    m = Member.query.filter_by(chat_id = chat_id, user_id = user_id).first()
    return m.id if m else None

def get_avatar_group(id: int):
    c = Chat.query.filter_by(id = id).first()
    return c.avatar if c else None

def check_chat_name(name1: str, name2: str):
    c = Chat.query.filter_by(chat_name = name1).first()
    id = c.id if c else None
    if id: 
        return id
    else:
        c = Chat.query.filter_by(chat_name = name2).first()
        return c.id if c else None
    
def check_group_joined(chat_id: int, user_id: int):
    m = Member.query.filter_by(chat_id = chat_id, user_id = user_id).first
    return m.id if m else None

def check_code(token: int):
    if token:
        c = Chat.query.filter_by(token = token).first()
        return c.id if c else None
    else: return None

def get_name_friend(id: int):
    u = User.query.filter_by(id=id).first()
    return u.name, u.lastname if u else None

def add_members(chat_id: int, user_id: int):
    role_id = 3
    m = Member(
        chat_id = chat_id,
        user_id = user_id,
        role_id = role_id)
    db.session.add(m)
    db.session.commit()
    return m.id

def get_chat_id(token: int):
    c = Chat.query.filter_by(token = token).first()
    return c.id if c else None

def get_avatar_friend(id: int):
    u = User.query.filter_by(id=id).first()
    return u.avatar if u else None
