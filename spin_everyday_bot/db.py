from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tg_id = db.Column(db.Integer(), nullable=False)
    username = db.Column(db.String())
    full_name = db.Column(db.String(), nullable=False)
    language = db.Column(db.String())
    wotd_registered = db.Column(db.Boolean(), nullable=False, default=False)
    wotd = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.id} "{self.full_name}" ("{self.username}")>'

    @property
    def effective_name(self):
        if self.username:
            return ('@' if not self.username.startswith('@') else '') + self.username
        return self.full_name or f'deleted id{self.id}'  # full name or deleted account


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tg_id = db.Column(db.Integer(), nullable=False)
    drawing_name = db.Column(db.String())
    winner_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    language = db.Column(db.String())
    timezone = db.Column(db.Integer(), nullable=False, default=0)
    auto_drawing = db.Column(db.Time())
    fast_drawing = db.Column(db.Boolean())
    admin_drawing = db.Column(db.Boolean())
    show_userlist = db.Column(db.Boolean())

    def __repr__(self):
        return f'<Chat {self.tg_id}>'


class ChatUser(db.Model):
    __tablename__ = 'chat_user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=False)
    chat_id = db.Column(db.Integer(), db.ForeignKey(Chat.id), nullable=False)
    can_change_name = db.Column(db.Boolean())
    win_count = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f'<ChatUser {self.user_id} in chat {self.chat_id}>'


class ChatText(db.Model):
    __tablename__ = 'chat_text'
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer(), db.ForeignKey(Chat.id))
    group = db.Column(db.Integer(), nullable=False)
    order = db.Column(db.Integer(), nullable=False)
    text = db.Column(db.String(), nullable=False)


__all__ = ('db', 'User', 'Chat', 'ChatUser', 'ChatText')
