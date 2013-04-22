import os
import pymongo
import bottle
import manage_users
import todo
import hs_auth

from urlparse import urlparse

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
    CONNECTION = pymongo.Connection(MONGO_URL, safe=True)
    db = CONNECTION[urlparse(MONGO_URL).path[1:]]
else:
    CONNECTION = pymongo.Connection('localhost', safe=True)
    db = CONNECTION.todolist

@bottle.route('/')
def default_login():
    """
    Checks if user is still logged in and redirects to todo page; otherwise,
    Produces login page
    """
    session = get_session()
    if session:
        return bottle.redirect('/todo')
    else:
        return bottle.redirect('/login')

@bottle.route('/login', method='GET')
def get_login_info():
    """
    Produces login page without error messages
    """
    return bottle.template('login', dict(user_error=None, pw_error=None))

@bottle.route('/login', method='POST')
def log_user_in():
    """
    Checks for Hacker School users and general users of the site.
    If the email and password match the database, redirects to todo page
    If user is a new Hacker Schooler with correct login info,
    adds them to the database
    If password is incorrect, asks them to retry
    If email is not recognized, asks them to sign_up for the email entered
    """
    email = bottle.request.forms.get('email')
    password = bottle.request.forms.get('password')

    hs_user_info = hs_auth.authenticate_with_hs(email, password)
    user_info = manage_users.get_info_from_db(email)

    user_error_msg = None
    pw_error_msg = None

    if hs_user_info or manage_users.email_matches_password(user_info, password):
        if hs_user_info:
            #user is a hackerschooler but isn't in my db
            username = "%s %s" % (hs_user_info['first_name'],
                    hs_user_info['last_name'])
            manage_users.add_user(email, username)

        session_id = manage_users.start_session(email)
        cookie = manage_users.get_cookie(session_id)
        bottle.response.set_cookie("session", cookie)
        bottle.redirect('/todo')
    else:
        if user_info:
            pw_error_msg = "Log in not successful; check your email/pw"
        else:
            user_error_msg = "We don't have that email in our db,"
        return bottle.template('login', dict(user_error = user_error_msg,
            pw_error = pw_error_msg))

@bottle.route('/signup', method='GET')
def get_user_and_pw():
    """
    Produces signup page without error messages
    """
    return bottle.template('signup', dict(pw_error = None, user_error = None))

@bottle.route('/signup', method='POST')
def store_user_and_pw():
    """
    Adds user to database and redirects to todo page
    Reproduces page with appropriate error message if:
     - passwords don't match, or
     - user is already in database
     """
    email = bottle.request.forms.get('email')
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    pwconf = bottle.request.forms.get('passwordconf')
    food = bottle.request.forms.get('food') #took this variable for fun

    if password == pwconf:
        user_error_check = manage_users.add_user(email,
                username, password, food)
        if not user_error_check:
            #Hooray, the pws match and the user is not in the system
            session_id = manage_users.start_session(email)
            cookie = manage_users.get_cookie(session_id)
            bottle.response.set_cookie("session", cookie)
            bottle.redirect('/todo')
        else:
            pw_error_message = "Your passwords do not match"
            return bottle.template('signup', dict(pw_error = None,
                user_error = user_error_check))
    else:
        return bottle.template('signup', dict(pw_error = pw_error_message,
            user_error = None))

@bottle.route('/anon', method='GET')
def explain_anon_to_user():
    """
    Before signing user in as "anonymous", explains the limitations.
    Then allows them to select anon or click on sign_in/login links
    """
    return bottle.template('anon')

@bottle.route('/anon', method='POST')
def create_anon_account():
    """
    Creates a session for a user with email "anon"
    """
    email = "anon"
    session_id = manage_users.start_session(email)
    cookie = manage_users.get_cookie(session_id)
    bottle.response.set_cookie("session", cookie)
    bottle.redirect('/todo')

@bottle.route('/welcome', method='GET')
def say_hello_to_my_friend():
    """
    Mostly a test page to see if user is recognized
    """
    session = get_session()
    email = session['email']
    user_info = manage_users.get_info_from_db(email)
    if user_info:
        username = user_info['username']
        food = user_info['food']
    elif email == "anon":
        username = "Anonymous"
        food = "food"
    return bottle.template('welcome', dict(username = username, food = food))

@bottle.route('/logout', method='GET')
def logout_user():
    """
    To log a user out, removes session from db and removes cookie
    """
    session = get_session()
    if session == None:
        bottle.redirect('/login', dict(user_error = None, pw_error = None))
    else:
        manage_users.end_session(session['_id'])
        bottle.response.set_cookie("session", "")
        bottle.redirect('/login')

def get_session():
    """
    Retrieves session from browser's stored cookie, if the session is valid
    """
    cookie = bottle.request.get_cookie("session")
    if not cookie:
        print "Sorry, no cookie in the cookie jar"
        return None
    else:
        session_id = manage_users.get_session_from_cookie(cookie)
        if not session_id:
            print "Sorry, your cookie didn't generate properly"
            return None
        else:
            session = manage_users.get_session_from_db(session_id)
    return session

if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
        PORT = int(os.environ.get('PORT', 5000))
        print "port = %d" % PORT
        bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        bottle.debug(True) #dev only, not for production
        bottle.run(host='localhost', port=8082, reloader=True) #dev only
