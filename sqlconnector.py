import sqlite3
import psycopg
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("psycopg")
logger.setLevel(logging.DEBUG)


def setup_connection(db='sqlite'):
    if db == 'sqlite':
        conn = setup_connection('postgresql')
    elif db == 'postgresql':
        conn = psycopg.connect("dbname=messager user=postgres password=15321 host=localhost")
    return conn

def select_info(login):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT id, username, name, lastname, bday, avatar, bio FROM users WHERE login=%s;", [login])
    rows = cur.fetchall()
    conn.close()
    if rows: return rows[0]
    else: return False

def create_user(login, name, last, bday, password, avatar, bio):
    if login and name and last and bday and password and avatar and bio:
        conn = setup_connection('postgresql')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (login, name, lastname, bday, avatar, bio) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;", (login, name, last, bday, avatar, bio))
        id = cur.fetchone()[0]
        cur.execute("INSERT INTO passwords (user_id, password) VALUES (%s, %s);", (id, password))
        conn.commit()
        conn.close()
        return True
    else: return False

def check_login(login):
    if login:
        conn = setup_connection('postgresql')
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE login=%s;", [login])
        id = cur.fetchone()
        conn.close()
        if id: return id[0]
        else: return None
    else: return None

def check_username(username):
    if username:
        conn = setup_connection('postgresql')
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s;", [username])
        id = cur.fetchone()
        conn.close()
        if id: return id[0]
        else: return None
    else: return None

def check_code(token):
    if token:
        conn = setup_connection('postgresql')
        cur = conn.cursor()
        cur.execute("SELECT id FROM chats WHERE token=%s;", [token])
        id = cur.fetchone()
        conn.close()
        if id: return id[0]
        else: return None
    else: return None

def check_group_joined(chat_id, user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM members WHERE user_id = %s AND chat_id = %s;", [user_id, chat_id])
    id = cur.fetchone()
    conn.close()
    if id: return True
    else: return None

def check_chat_name(name1, name2):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM chats WHERE chat_name=%s;", [name1])
    id = cur.fetchall()
    if id: 
        return id[0]
    else:
        cur.execute("SELECT id FROM chats WHERE chat_name=%s;", [name2])
        id = cur.fetchall()
        if id: 
            return id[0]
        else: 
            return None

def get_password(login):
    if login:
        conn = setup_connection('postgresql')
        cur = conn.cursor()
        cur.execute("SELECT passwords.password FROM users INNER JOIN passwords ON users.id = passwords.user_id WHERE users.login=%s;", [login])
        rows = cur.fetchone()
        conn.close()
        if rows: 
            return rows[0]
        else: 
            return None

def delete_user(login, user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE login=%s;", [login])
    cur.execute("DELETE FROM passwords WHERE user_id=%s;" [user_id])
    conn.commit()
    conn.close()
    return True

def edit_profile(login, avatar, name, lastname, username, bday, bio):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("UPDATE users SET avatar=%s, name=%s, lastname=%s, username=%s, bday=%s, bio=%s WHERE login=%s;", [avatar, name, lastname, username, bday, bio, login])
    conn.commit()
    conn.close()
    return True

def create_chat(creator_id, chat_name, type_chat, role_id, chat_state_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("INSERT INTO chats (creator_id, chat_name, type_id) VALUES (%s, %s, %s) RETURNING *;", [creator_id, chat_name, type_chat])
    conn.commit()
    # print('STATUS: ', conn.info.transaction_status)
    chat_id = cur.fetchone()[0]
    # print('create_chat sql: ', chat_id)
    cur.execute("INSERT INTO members (chat_id, user_id, role_id, chat_state_id) VALUES (%s, %s, %s, %s);", [chat_id, creator_id, role_id, chat_state_id])
    conn.commit()
    conn.close()
    return chat_id

def add_avatar_chat(chat_id, avatar):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("UPDATE chats SET avatar=%s WHERE id = %s;", [avatar, chat_id])
    conn.commit()
    conn.close()
    return True

def add_token_chat(chat_id, token):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("UPDATE chats SET token=%s WHERE id = %s;", [token, chat_id])
    conn.commit()
    conn.close()
    return True

def get_chat_id(token):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM chats WHERE token = %s;", [token])
    id = cur.fetchone()
    conn.close()
    if id: 
        return id[0]
    else: 
        return None

def join_group(chat_id, user_id, role_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("INSERT INTO members (chat_id, user_id, role_id) VALUES (%s, %s, %s);", [chat_id, user_id, role_id])
    conn.commit()
    conn.close()
    return True

def add_members(chat_id, user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    role_id = 3
    cur.execute("INSERT INTO members (chat_id, user_id, role_id) VALUES (%s, %s, %s);", [chat_id, user_id, role_id])
    conn.commit()
    conn.close()
    return True

def save_message(msg, type_id, timestamp, member_id, chat_id, state_id, content_state_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("INSERT INTO message_entries (message, type_id, timestamp, member_id, chat_id, state_id, content_state_id) VALUES (%s, %s, %s, %s, %s, %s, %s);", [msg, type_id, timestamp, member_id, chat_id, state_id, content_state_id])
    conn.commit()
    conn.close()
    return True

def get_messages(chat_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute('''SELECT message_entries.id, message_entries.message, message_entries.type_id, 
                message_entries.timestamp, users.id, message_entries.chat_id, message_entries.state_id, 
                message_entries.content_state_id, chats.type_id, users.avatar
                FROM message_entries 
                INNER JOIN members ON message_entries.member_id = members.id
                INNER JOIN users ON members.user_id = users.id
				INNER JOIN chats ON chats.id = message_entries.chat_id
                WHERE message_entries.chat_id = %s;''', [chat_id])
    msg_inf = cur.fetchall()
    if msg_inf:
        return msg_inf
    else:
        return None
    
def get_member_id(chat_id, user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT id FROM members WHERE chat_id = %s AND user_id = %s;", [chat_id, user_id])
    member_id = cur.fetchone()
    conn.close()
    if member_id: 
        return member_id[0]
    else: 
        return None

def get_name_friend(id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT name, lastname FROM users WHERE id = %s;", [id])
    name = cur.fetchall()
    conn.close()
    if name: 
        return name[0]
    else: 
        return None

def get_avatar_friend(id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT avatar FROM users WHERE id = %s;", [id])
    img = cur.fetchone()
    conn.close()
    if img: 
        return img[0]
    else: 
        return None

def get_avatar_group(id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT avatar FROM chats WHERE id = %s;", [id])
    img = cur.fetchone()
    conn.close()
    if img: 
        return img[0]
    else: 
        return None
    
def get_chat_name_type(id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT name, type_id FROM chats WHERE id = %s;", [id])
    inf = cur.fetchone()
    conn.close()
    name = inf[0]
    id = inf[1]
    if id == 1: type = 'personal'
    else: type = 'group'
    if type: 
        return name, type
    else: 
        return None
    
# ORDER BY message_entries.timestamp DESC
def get_chat_list(user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute('''SELECT members.chat_id, chats.chat_name, chats.type_id, members.chat_state_id, members.role_id, message_entries.message, MAX(message_entries.timestamp)
    FROM members
    INNER JOIN chats
    ON chats.id = members.chat_id
    INNER JOIN message_entries
    ON message_entries.chat_id = chats.id
    WHERE members.user_id = %s
    AND message_entries.timestamp = (
	 	SELECT MAX(message_entries.timestamp)
	 	FROM message_entries
	 	WHERE message_entries.chat_id = members.chat_id)
    GROUP BY members.chat_id, chats.chat_name, chats.type_id, members.chat_state_id, members.role_id, message_entries.message, message_entries.timestamp
    ORDER BY message_entries.timestamp
	DESC;''', [user_id])
    
    inf = cur.fetchall()
    conn.close()
    # print("INF BAZE: ", inf)
    if inf: 
        return inf
    else: 
        return None

def get_chat_list_empty(user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    # print('USER_ID get_chat_list_emtu BAZE: ', user_id)
    cur.execute('''SELECT members.chat_id, chats.chat_name, chats.type_id, members.chat_state_id, members.role_id
                FROM members
                INNER JOIN chats
				ON chats.id = members.chat_id
                WHERE members.user_id = %s
                AND (SELECT COUNT(message_entries.id)
                FROM message_entries
				WHERE message_entries.chat_id = chats.id) = 0''', [user_id])
    inf = cur.fetchall()
    conn.close()
    # print("INF_EMPTY: ", inf)
    if inf: 
        return inf
    else: 
        return None

def get_chat_inf(target, id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    if target == "name":
        cur.execute("SELECT chat_name FROM chats WHERE id = %s;", [id])
    elif target == "creator":
        cur.execute("SELECT creator_id FROM chats WHERE id = %s;", [id])
    elif target == "date":
        cur.execute("SELECT date_of_creation FROM chats WHERE id = %s;", [id])
    elif target == "token":
        cur.execute("SELECT token FROM chats WHERE id = %s;", [id])
    elif target == "type":
        cur.execute("SELECT type_id FROM chats WHERE id = %s;", [id])
    elif target == "avatar":
        cur.execute("SELECT avatar FROM chats WHERE id = %s;", [id])
    inf = cur.fetchone()
    conn.close()
    if inf: 
        return inf[0]
    else: 
        return None

def get_chat_state_id(chat_id, user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT chat_state_id FROM members WHERE chat_id = %s AND user_id = %s;", [chat_id, user_id])
    state_id = cur.fetchone()
    conn.close()
    if state_id:
        return state_id[0]
    else:
        return None

def get_role_id(chat_id, user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT role_id FROM members WHERE chat_id = %s AND user_id = %s;", [chat_id, user_id])
    role_id = cur.fetchone()
    conn.close()
    if role_id:
        return role_id[0]
    else:
        return None

def get_last_msg(chat_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT message, timestamp FROM message_entries WHERE chat_id = %s ORDER BY id DESC LIMIT 1;", [chat_id])
    msg_inf = cur.fetchall()
    conn.close()
    if msg_inf:
        return msg_inf[0]
    else:
        return None

def cnt_members(chat_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM members WHERE chat_id=%s;", [chat_id])
    cnt_members = cur.fetchone()
    conn.close()
    if cnt_members: 
        return cnt_members[0]
    else: 
        return None

def get_members(chat_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute('''SELECT users.name, users.lastname, users.avatar
                FROM users
                INNER JOIN members
                ON members.user_id = users.id
                WHERE members.chat_id=%s;''', [chat_id])
    members = cur.fetchone()
    conn.close()
    if members: 
        return members[0]
    else: 
        return None

def block_user(chat_id, friend_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("UPDATE members SET chat_state_id=%s WHERE chat_id=%s and user_id=%s;", [2, chat_id, friend_id])
    conn.commit()
    conn.close()
    return True

def unblock_user(chat_id, friend_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("UPDATE members SET chat_state_id=%s WHERE chat_id=%s AND user_id=%s;", [1, chat_id, friend_id])
    conn.commit()
    conn.close()
    return True

def leave_chat(chat_id, user_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE chat_id=%s AND user_id=%s;", [chat_id, user_id])
    conn.commit()
    conn.close()
    return True

def clear_chat(chat_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("DELETE FROM message_entries WHERE chat_id=%s;", [chat_id])
    conn.commit()
    conn.close()
    return True

def delete_chat(chat_id):
    conn = setup_connection('postgresql')
    cur = conn.cursor()
    cur.execute("DELETE FROM chats WHERE id=%s;", [chat_id])
    conn.commit()
    conn.close()
    return True

