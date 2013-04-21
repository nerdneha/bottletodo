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

@bottle.route('/todo', method='GET')
def todo_list():
    """
    Produces all tasks in categories "open" and "closed" tasks for any user
    """
    open_tasks = db.tasks.find({'status':1})
    closed_tasks = db.tasks.find({'status':0})
    output = bottle.template('make_list', open_rows = open_tasks,
                    closed_rows = closed_tasks)
    return output

@bottle.route('/add', method='GET')
def enter_new_item():
    """
    Displays page for adding a new task for any user
    """
    return bottle.template('new_task', error_msg = None)

@bottle.route('/add', method='POST')
def save_new_item():
    """
    Saves the new item into the database and redirects to main list for validated users
    Produces error message for anon or invalid users
    """
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
    """
    Allows users to edit a task's name and status based on task ID number
    Invalid users can edit but can't save the changes
    """
    cur_task = db.tasks.find_one({'_id': number})
    return bottle.template('edit_task', old=cur_task,
            num=number, error_msg=None)

@bottle.route('/edit', method='POST')
def todo_save():
    """
    Saves the edited item into the database and redirects to main list for validated users
    Produces error message for anon or invalid users
    """
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
        cur_task = db.tasks.find_one({'_id': int(num)})
        return bottle.template('edit_task', old=cur_task,
                num=num, error_msg="Sorry you cannot add tasks because you are not signed in as a user or because of a cookie error")

@bottle.route('/change/:num/:status')
def change_status(num, status):
    """
    Changes a status from open --> closed and vice versa for any user
    """
    db.tasks.update({'_id': int(num)}, {'$set': {'status': int(status)}})
    return bottle.redirect('/todo')

@bottle.error(404)
def mistake404(code):
    """
    Simple error message for a 404 code
    """
    return 'Sorry, this page does not exist! Site error message: ', code

@bottle.error(403)
def mistake403(code):
    """
    Simple error message for a 403 code
    """
    return 'The parameter you passed has the wrong format! Site error message: ', code


if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
        PORT = int(os.environ.get('PORT', 5000))
        print "port = %d" % PORT
        bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        bottle.debug(True) #dev only, not for production
        bottle.run(host='localhost', port=8082, reloader=True) #dev only
