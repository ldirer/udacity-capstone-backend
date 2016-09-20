from sqlalchemy.sql.schema import ForeignKey

from g import db


class Language(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    icon_name = db.Column(db.String)
    microsoft_name = db.Column(db.String)


class UserLanguage(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user._id"), nullable=False)
    language_id = db.Column(db.Integer, ForeignKey("language._id"), nullable=False)


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    google_id = db.Column(db.String)
    languages = db.relationship(Language, secondary=UserLanguage.__table__, backref=db.backref('users'))


class Word(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, ForeignKey("language._id"))
    word = db.Column(db.String)
    translation = db.Column(db.String)

    language = db.relationship(Language, backref=db.backref('words'))


    def json(self):
        pass


class Attempt(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, ForeignKey("word._id"))
    user_id = db.Column(db.Integer, ForeignKey("user._id"))
    success = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)


