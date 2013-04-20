import hashlib
import random
import string
import hmac
import bson
import os
import pymongo
import sys
from urlparse import urlparse

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
    CONNECTION = pymongo.Connection(MONGO_URL, safe=True)
    db = CONNECTION[urlparse(MONGO_URL).path[1:]]
else:
    CONNECTION = pymongo.Connection('localhost', safe=True)
    db = CONNECTION.todolist

def make_salt():
    """
    Creates a salt by selecting 5 random letters
    """
    salt = ""
    for i in range(5):
        salt += random.choice(string.ascii_letters)
    return salt

def hash_pw(password, salt=None):
    """
    Creates a salt and hashes password with salt
    """
    if salt == None:
        salt = make_salt()
    return "%s,%s" % (hashlib.sha1(password+salt).hexdigest(), salt)

def add_user(email, username, password=None, food=None):
    """
    Adds or udpates a user in the database
    """
    try:
        db.users.update({'_id': email}, {'$set':
            {'username': username}}, upsert=True)
        if password:
            hashed_pw = hash_pw(password)
            db.users.update({'_id': email}, {'$set':
                {'password': hashed_pw}})
        if food:
            db.users.update({'_id': email}, {'$set':
                {'food': food}})

    except pymongo.errors.DuplicateKeyError:
        #users.
        return "You're already in the database" % (email)
    except:
        return "Pymongo error, retry"

def start_session(email):
    """
    Records the start of a session to keep track of user
    """
    sessions = db.sessions
    session = {"email": email}
    try:
        sessions.insert(session)
    except pymongo.errors.PyMongoError:
        print "Unexpected error on start_session:", sys.exc_info()[0]
        return -1
    return str(session['_id'])

KEYWORD = "HASH ME"
def hash_string(string_to_hash):
    """
    Hash the string with a keyword
    """
    return hmac.new(KEYWORD, string_to_hash).hexdigest()

def get_cookie(session_id):
    """
    Hashes the session_id as the cookie
    """
    return "%s|%s" % (session_id, hash_string(session_id))

def get_session_from_cookie(cookie):
    """
    Extracts session_id from cookie
    """
    session_id = cookie.split("|")[0]
    if (get_cookie(session_id) == cookie):
        return session_id

def get_session_from_db(session_id):
    """
    Retrieves session from db
    """
    sessions = db.sessions
    try:
        object_id = bson.objectid.ObjectId(session_id)
        session = sessions.find_one({'_id': object_id})
    except pymongo.errors.PyMongoError:
        print "Had issues retrieving your session_id from the db"
    return session

def get_info_from_db(email):
    """
    Retrieves user info from db based on user_id/email
    """
    #determines if email is in local database
    users = db.users
    try:
        user_info = users.find_one({'_id': email})
        return user_info
    except pymongo.errors.PyMongoError:
        print "Need to create a new acct"
        return None

def email_matches_password(user_info, password):
    """
    Verifies if a username matches the password stored in the db
    """
    db_password = user_info['password']
    past_salt = db_password.split(",")[1]
    return hash_pw(password, past_salt) == db_password

def end_session(session_id):
    """
    Removes session from db
    """
    sessions = db.sessions
    try:
        object_id = bson.objectid.ObjectId(session_id)
        sessions.remove({'_id': object_id})
    except pymongo.errors.PyMongoError:
        print "unable to remove session"
    return
