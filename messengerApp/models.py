from .extensions import db
import datetime
 
class ChatState(db.Model):
    __tablename__ = 'chat_states'
    id    = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Text, nullable=False)
 
    members = db.relationship('Member', back_populates='chat_state', cascade='all, delete')
 
class ChatType(db.Model):
    __tablename__ = 'chat_types'
    id   = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False)
 
    chats = db.relationship('Chat', back_populates='chat_type', cascade='all, delete')
 
class EntryType(db.Model):
    __tablename__ = 'entry_types'
    id   = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False)
 
    message_entries = db.relationship('MessageEntry', back_populates='entry_type', cascade='all, delete')
 
class MessageContentState(db.Model):
    __tablename__ = 'message_content_states'
    id    = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Text, nullable=False)
 
    message_entries = db.relationship('MessageEntry', back_populates='content_state', cascade='all, delete')
 
class MessageState(db.Model):
    __tablename__ = 'message_states'
    id    = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Text, nullable=False)
 
    message_entries = db.relationship('MessageEntry', back_populates='state', cascade='all, delete')
 
class Role(db.Model):
    __tablename__ = 'roles'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
 
    members = db.relationship('Member', back_populates='role', cascade='all, delete')
 
class User(db.Model):
    __tablename__ = 'users'
    id        = db.Column(db.Integer, primary_key=True)
    login     = db.Column(db.Text, nullable=False, unique=True)
    username  = db.Column(db.Text, unique=True)
    name      = db.Column(db.Text, nullable=False)
    lastname  = db.Column(db.Text, nullable=False)
    bday      = db.Column(db.Date, nullable=False)
    avatar    = db.Column(db.Text)
    bio       = db.Column(db.Text)
 
    passwords = db.relationship('Password', back_populates='user', cascade='all, delete')
    chats     = db.relationship('Chat',     back_populates='creator', cascade='all, delete')
    members   = db.relationship('Member',   back_populates='user',    cascade='all, delete')
 
class Chat(db.Model):
    __tablename__ = 'chats'
    id              = db.Column(db.Integer, primary_key=True)
    creator_id      = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    chat_name       = db.Column(db.Text, nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    token           = db.Column(db.Text, unique=True)
    type_id         = db.Column(db.Integer, db.ForeignKey('chat_types.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    avatar          = db.Column(db.Text)
 
    creator         = db.relationship('User',      back_populates='chats')
    chat_type       = db.relationship('ChatType',  back_populates='chats')
    members         = db.relationship('Member',    back_populates='chat', cascade='all, delete')
    message_entries = db.relationship('MessageEntry', back_populates='chat', cascade='all, delete')
 
class Member(db.Model):
    __tablename__ = 'members'
    id            = db.Column(db.Integer, primary_key=True)
    chat_id       = db.Column(db.Integer, db.ForeignKey('chats.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    role_id       = db.Column(db.Integer, db.ForeignKey('roles.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    chat_state_id = db.Column(db.Integer, db.ForeignKey('chat_states.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, default=1)
 
    chat          = db.relationship('Chat',      back_populates='members')
    user          = db.relationship('User',      back_populates='members')
    role          = db.relationship('Role',      back_populates='members')
    chat_state    = db.relationship('ChatState', back_populates='members')
    message_entries = db.relationship('MessageEntry', back_populates='member', cascade='all, delete')
 
class MessageEntry(db.Model):
    __tablename__ = 'message_entries'
    id               = db.Column(db.Integer, primary_key=True)
    message          = db.Column(db.Text, nullable=False)
    type_id          = db.Column(db.Integer, db.ForeignKey('entry_types.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    timestamp        = db.Column('timestamp', db.DateTime, nullable=False)
    member_id        = db.Column(db.Integer, db.ForeignKey('members.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    chat_id          = db.Column(db.Integer, db.ForeignKey('chats.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    state_id         = db.Column(db.Integer, db.ForeignKey('message_states.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    content_state_id = db.Column(db.Integer, db.ForeignKey('message_content_states.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
 
    entry_type    = db.relationship('EntryType',           back_populates='message_entries')
    member        = db.relationship('Member',              back_populates='message_entries')
    chat          = db.relationship('Chat',                back_populates='message_entries')
    state         = db.relationship('MessageState',        back_populates='message_entries')
    content_state = db.relationship('MessageContentState', back_populates='message_entries')
 
class Password(db.Model):
    __tablename__ = 'passwords'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    password      = db.Column(db.Text, nullable=False)
 
    user          = db.relationship('User', back_populates='passwords')
 