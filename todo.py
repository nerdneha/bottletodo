import os
import pymongo
import bottle
import sign_up
import manage_users
from urlparse import urlparse

MONGO_URL = os.environ.get('MONGOHQ_URL')
#print os.environ.get('MONGOHQ_URL')
if MONGO_URL:
  connection = pymongo.Connection(MONGO_URL, safe=True)
  db = connection[urlparse(MONGO_URL).path[1:]]
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.todolist
tasks = db.tasks

@bottle.route('/')
def start_at_todo():
  return bottle.redirect('/signup')

@bottle.route('/todo', method='GET')
def todo_list():
  #print_list(tasks.find())
  session = sign_up.get_session()
  open_tasks = tasks.find({'status':1})
  closed_tasks = tasks.find({'status':0})
  output = bottle.template('make_list', open_rows = open_tasks,
                    closed_rows = closed_tasks)
  return output

@bottle.route('/add', method='GET')
def enter_new_item():
    return bottle.template('new_task')

@bottle.route('/add', method='POST')
def save_new_item():
  new = bottle.request.forms.get('task', '').strip()
  new_id = tasks.count() + 1
  session = sign_up.get_session()
  username = session['username']
  user_info = manage_users.get_user_info(username)
  food = user_info['food']
  tasks.insert({"_id": new_id, "task": new, "status": 1, "username": username,
                "food": food})#POST THIS
  return bottle.redirect('/todo')

@bottle.route('/edit/:no', method='GET')
@bottle.validate(no=int)
def edit_item(no):
  cur_data = tasks.find_one({'_id': no})
  return bottle.template('edit_task', old=cur_data, no=no)

@bottle.route('/edit', method='POST')
def todo_save():
  edit = bottle.request.forms.get('task','').strip()
  status = bottle.request.forms.get('status','').strip()
  no = bottle.request.forms.get('no','').strip()
  #print no, type(no)
  if status == 'open':
    status = 1
  else:
    status = 0
  tasks.update({'_id': int(no)}, {'$set': {'task': edit, 'status': status}})
  #print tasks.find_one({'_id': no})
  return bottle.redirect('/todo')

@bottle.route('/item:item#[1-9]+#')
def show_item(item):
  result = tasks.find_one({'_id': int(item)})
  if not result:
    return 'This item number does not exist!'
  else:
    return 'Task: %s' %result['task']

# show_item = bottle.route('/item:item#[1-9]+#')(show_item)

@bottle.route('/json:number#[1-9]+#')
def show_json(number):
  result = tasks.find_one({'_id': int(number)})
  if not result:
    return {'task':'This item number does not exist!'}
  else:
    return result

@bottle.route('/change/:no/:status')
def change_status(no, status):
  tasks.update({'_id': int(no)}, {'$set': {'status': int(status)}})
  #print "tried to updated item " + no
  return bottle.redirect('/todo')

@bottle.error(404)
def mistake404(code):
  return 'Sorry, this page does not exist!'

@bottle.error(403)
def mistake403(code):
  return 'The parameter you passed has the wrong format!'

def print_list(mongo_list):
  print "printing list"
  for item in mongo_list:
    print item

if __name__ == '__main__':
  if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
    port = int(os.environ.get('PORT', 5000))
    print "port = %d" % port
    bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  else:
    bottle.debug(True) #dev only, not for production
    bottle.run(host='localhost', port=8082, reloader=True) #dev only
