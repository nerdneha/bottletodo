import pymongo
import os
import hashlib
import random
import string
import hmac
import bson

MONGO_URL = os.environ.get('MONGOHQ_URL')
if MONGO_URL:
  connection = pymongo.Connection(MONGO_URL, safe=True)
  db = connection[urlparse(MONGO_URL).path[1:]]
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.todolist

def check_if_pws_match(password, pwconf):
  if password != pwconf:
    return "Your passwords do not match"

def make_salt():
  salt = ""
  for i in range(5):
    salt += random.choice(string.ascii_letters)
  return salt

def hash_pw(password, salt=None):
  if salt == None:
    salt = make_salt()
  return "%s,%s" % (hashlib.sha1(password+salt).hexdigest(), salt)

def add_user(username, password, food):
  hashed_pw = hash_pw(password)
  try:
    users = db.users
    users.insert({"_id": username, "password": hashed_pw, "food": food})
  except pymongo.errors.DuplicateKeyError as e:
    return "Username %s is already used, if that's you:" % (username)
  except:
    return "Pymongo error, retry"

def start_session(username):
  sessions = db.sessions
  session = {"username": username}
  try:
    sessions.insert(session)
  except:
    print "Unexpected error on start_session:", sys.exc_info()[0]
    return -1
  return str(session['_id'])

KEYWORD = "HASH ME"
def hash_string(string_to_hash):
  return hmac.new(KEYWORD, string_to_hash).hexdigest()

def get_cookie(session_id):
  #hashes the session_id as the cookie
  return "%s|%s" % (session_id, hash_string(session_id))

def get_session_from_cookie(cookie):
  session_id = cookie.split("|")[0]
  if (get_cookie(session_id) == cookie):
    return session_id

def get_session_from_db(session_id):
  sessions = db.sessions
  try:
    object_id = bson.objectid.ObjectId(session_id)
    session = sessions.find_one({'_id': object_id})
  except:
    print "Had issues retrieving your session_id from the db"
  return session

def get_user_info(username):
  users = db.users
  try:
    user_info = users.find_one({'_id': username})
  except:
    print "Couldn't retrieve your username from the db"
  return user_info

def username_matches_password(user_info, password):
  pw = user_info['password']
  past_salt = pw.split(",")[1]
  return hash_pw(password, past_salt) == pw

def end_session(session_id):
  sessions = db.sessions
  try:
    object_id = bson.objectid.ObjectId(session_id)
    sessions.remove({'_id': object_id})
  except:
    print "unable to remove session"
  return
