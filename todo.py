import os
import pymongo
import bottle
import sign_up
import manage_users
from urlparse import urlparse

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
    CONNECTION = pymongo.Connection(MONGO_URL, safe=True)
    db = CONNECTION[urlparse(MONGO_URL).path[1:]]
else:
    CONNECTION = pymongo.Connection('localhost', safe=True)
    db = CONNECTION.todolist

@bottle.route('/')
def start_at_todo():
    return bottle.redirect('/signup')

@bottle.route('/todo', method='GET')
def todo_list():
    open_tasks = db.tasks.find({'status':1})
    closed_tasks = db.tasks.find({'status':0})
    output = bottle.template('make_list', open_rows = open_tasks,
                    closed_rows = closed_tasks)
    return output

@bottle.route('/add', method='GET')
def enter_new_item():
    return bottle.template('new_task', error_msg = None)

@bottle.route('/add', method='POST')
def save_new_item():
    new = bottle.request.forms.get('task', '').strip()
    new_id = db.tasks.count() + 1
    #verify user
    session = sign_up.get_session()
    email = session['email']
    user_info = manage_users.get_info_from_db(email)
    if user_info:
        db.tasks.insert({"_id": new_id, "task": new, "status": 1, "username": user_info['username']})
        if 'food' in user_info:
            db.tasks.update({"_id": new_id}, {"$set": {"food": user_info['food']}})
        return bottle.redirect('/todo')
    else:
        return bottle.template('new_task',
                error_msg = "Sorry you cannot add tasks because you are not signed in as a user or because of a cookie error")


@bottle.route('/edit/:number', method='GET')
@bottle.validate(number=int)
def edit_item(number):
    cur_data = db.tasks.find_one({'_id': number})
    return bottle.template('edit_task', old=cur_data,
            num=number, error_msg=None)

@bottle.route('/edit', method='POST')
def todo_save():
    edit = bottle.request.forms.get('task','').strip()
    status = bottle.request.forms.get('status','').strip()
    num = bottle.request.forms.get('num','').strip()
    if status == 'open':
        status = 1
    else:
        status = 0
    #verify user
    session = sign_up.get_session()
    email = session['email']
    user_info = manage_users.get_info_from_db(email)
    if user_info:
        db.tasks.update({'_id': int(num)}, {'$set':
            {'task': edit, 'status': status}})
        return bottle.redirect('/todo')
    else:
        return bottle.template('edit_task', old=db.tasks.fine_one({'_id': num}),
                num=num, error_msg="Sorry you cannot add tasks because you are not signed in as a user or because of a cookie error")

@bottle.route('/change/:no/:status')
def change_status(no, status):
    db.tasks.update({'_id': int(no)}, {'$set': {'status': int(status)}})
    return bottle.redirect('/todo')

@bottle.error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

@bottle.error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'

if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
        port = int(os.environ.get('PORT', 5000))
        print "port = %d" % port
        bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        bottle.debug(True) #dev only, not for production
        bottle.run(host='localhost', port=8082, reloader=True) #dev only
