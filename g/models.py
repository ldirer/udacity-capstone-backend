from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy

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
    created_timestamp = db.Column(db.DateTime(), index=True)
    language = db.relationship(Language)

    def language_name(self):
        return self.language.name


class Word(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, ForeignKey("language._id"))
    word = db.Column(db.String)
    translation = db.Column(db.String)
    language = db.relationship(Language, backref=db.backref('words'))


class Attempt(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, ForeignKey("word._id"))
    word = db.relationship(Word)
    # This is lame. I want this key in my JSON (it's nice to have it in the sqlite db to avoid an extra join).
    # However I dont know how to include it as a 'computed attribute on the Word relationship'. So quick and dirty. And unsecure.
    # language_id = db.Column(db.Integer)

    # Here's the right solution! unfortunately it does not appear in flask-restless response anymore... I'm hacking this with a selector method and the `include_methods` parameter on create_api.
    # language_id = association_proxy('word', 'language_id')
    user_id = db.Column(db.Integer, ForeignKey("user._id"))
    success = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def language_id(self):
        """This simple method and the `include_methods` parameter on `create_api` looks like the best solution."""
        # Initially I was doing: return self.language_id
        # Actually we should do self.word.language_id. The association proxy is not useful here, it would be if we wanted to update the word language id directly from the attempt.
        # Leaving it commented cause association proxies are cool.
        return self.word.language_id


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    google_id = db.Column(db.String, index=True)
    # languages = db.relationship(Language, secondary=UserLanguage.__table__, backref=db.backref('users'))
    languages = db.relationship(UserLanguage, backref=db.backref('user'))
    attempts = db.relationship(Attempt, backref=db.backref('user'))
    created_timestamp = db.Column(db.DateTime(), index=True)
# # It would probably have been more flexible to have an Update table along the lines of:
# class Update(db.Model):
#     timestamp = db.Column(db.DateTime(), index=True)
#     object_id = ...
#     object_type = ...
# This would allow us to get the last_update timestamp in just one query.


