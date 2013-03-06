import os
import pymongo
import bottle
import manage_users
import todo
from urlparse import urlparse

MONGO_URL = os.environ.get('MONGOHQ_URL')
print "MONGO_URL = %s" % (MONGO_URL)
print "ENVIRON VAR = %s" % (os.environ.get('ENVIRONMENT'))

if MONGO_URL:
  connection = pymongo.Connection(MONGO_URL, safe=True)
  db = connection[urlparse(MONGO_URL).path[1:]]
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.todolist

@bottle.route('/')
def default_go_to_signup():
  #eventually ask if there's a cookie so i can redirect to a logged in page
  return bottle.redirect('/signup')

@bottle.route('/signup', method='GET')
def get_user_and_pw():
  return bottle.template('signup', dict(pw_error = "", user_error = ""))

@bottle.route('/signup', method='POST')
def store_user_and_pw():
  username = bottle.request.forms.get('username')
  password = bottle.request.forms.get('password')
  pwconf = bottle.request.forms.get('passwordconf')
  food = bottle.request.forms.get('food') #took this variable for fun

  pw_error_message = "Your passwords do not match"

  if password == pwconf:
    user_error_check = manage_users.add_user(username, password, food)
    if user_error_check == None:
      entry = db.users.find_one({"_id": username})
      hashed_pw = entry["password"]
      #Houston we are a go, the pws match and the user is not in the system
      #THIS IS WHERE THE MAGIC HAPPENS
      session_id = manage_users.start_session(username)
      cookie = manage_users.get_cookie(session_id)
      bottle.response.set_cookie("session", cookie)
      bottle.redirect('/todo')
    else:
      return bottle.template('signup', dict(pw_error = "", user_error =
                                            user_error_check))
  else:
    return bottle.template('signup', dict(pw_error = pw_error_message, user_error = ""))

def get_session():
  cookie = bottle.request.get_cookie("session")
  if cookie == None:
    print "Sorry, no cookie in the cookie jar"
    return None
  else:
    session_id = manage_users.get_session_from_cookie(cookie)
    if (session_id == None):
      print "Sorry, your cookie didn't generate properly"
      return None
    else:
      session = manage_users.get_session_from_db(session_id)
  return session

@bottle.route('/login', method='GET')
def get_login_info():
  return bottle.template('login', dict(user_error="", pw_error=""))

@bottle.route('/login', method='POST')
def log_user_in():
  username = bottle.request.forms.get('username')
  password = bottle.request.forms.get('password')

  user_info = manage_users.get_user_info(username)
  if user_info != None:
    if manage_users.username_matches_password(user_info, password):
      #houston we are a go, start a new session
      session_id = manage_users.start_session(username)
      cookie = manage_users.get_cookie(session_id)
      bottle.response.set_cookie("session", cookie)
      bottle.redirect('/todo')
    else:
      error_message = "Your username didn't match your pw, retry?"
      return bottle.template('login', dict(user_error = "", pw_error = error_message))
  else:
    error_message = "Your username doesn't exist:"
    return bottle.template('login', dict(user_error = error_message, pw_error = ""))

@bottle.route('/welcome', method='GET')
def say_hello_to_my_friend():
  session = get_session()
  username = session['username']
  user_info = manage_users.get_user_info(username)
  food = user_info['food']
  return bottle.template('welcome', dict(username = username, food = food))

@bottle.route('/logout', method='GET')
def logout_user():
  session = get_session()
  if session == None:
    bottle.redirect('/login', dict(user_error = "", pw_error = ""))
  else:
    manage_users.end_session(session['_id'])
    bottle.response.set_cookie("session", "")
    bottle.redirect('/login')

if __name__ == '__main__':
  if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
    port = int(os.environ.get('PORT', 5000))
    print "port = %d" % port
    bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  else:
    bottle.debug(True) #dev only, not for production
    bottle.run(host='localhost', port=8082, reloader=True) #dev only
