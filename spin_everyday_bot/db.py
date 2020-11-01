#  SpinEverydayBot
#  Copyright © 2016-2017, 2020 Evgeniy Filimonov <evgfilim1@yandex.ru>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = 'users'
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
        return self.full_name or f'deleted (id{self.id})'  # full name or deleted account


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tg_id = db.Column(db.Integer(), nullable=False)
    drawing_name = db.Column(db.String())
    winner_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    language = db.Column(db.String())
    timezone = db.Column(db.Integer(), nullable=False, default=0)
    auto_drawing = db.Column(db.Time())
    fast_drawing = db.Column(db.Boolean())
    admin_drawing = db.Column(db.Boolean())
    opt_in_drawing = db.Column(db.Boolean())
    show_userlist = db.Column(db.Boolean())

    def __repr__(self):
        return f'<Chat {self.tg_id}>'


class ChatUser(db.Model):
    __tablename__ = 'chat_users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=False)
    chat_id = db.Column(db.Integer(), db.ForeignKey(Chat.id), nullable=False)
    can_change_name = db.Column(db.Boolean())
    win_count = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f'<ChatUser {self.user_id} in chat {self.chat_id}>'


class WinHistoryItem(db.Model):
    __tablename__ = 'win_history'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    chat_user_id = db.Column(db.Integer(), db.ForeignKey(ChatUser.id), nullable=False)
    win_date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f'<WinHistoryItem at {self.win_date} for {self.chat_user_id}>'


class ChatText(db.Model):
    __tablename__ = 'chat_texts'
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer(), db.ForeignKey(Chat.id))
    group = db.Column(db.Integer(), nullable=False)
    order = db.Column(db.Integer(), nullable=False)
    text = db.Column(db.String(), nullable=False)


__all__ = ('db', 'User', 'Chat', 'ChatUser', 'ChatText')
