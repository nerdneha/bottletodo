import pymongo
import bottle

connection = pymongo.Connection('localhost', safe=True)
db=connection.todolist
tasks = db.tasks

@bottle.route('/')
def start_at_todo():
  return bottle.redirect("/todo")

@bottle.route('/todo', method='POST')
def todo_save():
    edit = bottle.request.forms.get('task','').strip()
    status = bottle.request.forms.get('status','').strip()
    no = bottle.request.forms.get('no','').strip()
    print no, type(no)
    if status == 'open':
      status = 1
    else:
      status = 0
    tasks.update({'_id': int(no)}, {'task': edit, 'status': status})
    print tasks.find_one({'_id': no})
    return bottle.redirect("/todo")

@bottle.route('/todo', method='GET')
def todo_list():
  #print_list(tasks.find())
  open_tasks = tasks.find({'status':1})
  closed_tasks = tasks.find({'status':0})
  output = bottle.template('make_list', open_rows=open_tasks,
                    closed_rows=closed_tasks)
  return output

@bottle.route('/add', method='GET')
def new_item_mongo():
  if bottle.request.GET.get('save','').strip():
    new = bottle.request.GET.get('task', '').strip()
    new_id = tasks.count() + 1
    tasks.insert({"_id": new_id, "task": new, "status": 1})
    return bottle.redirect("/todo")
  else:
    return bottle.template('new_task')

@bottle.route('/edit/:no', method='GET')
@bottle.validate(no=int)
def edit_item(no):
  cur_data = tasks.find_one({'_id': no})
  return bottle.template('edit_task', old=cur_data, no=no)

@bottle.route('/item:item#[1-9]+#')
def show_item(item):
  result = tasks.find_one({'_id': int(item)})
  if not result:
    return 'This item number does not exist!'
  else:
    return 'Task: %s' %result['task']

# show_item = bottle.route('/item:item#[1-9]+#')(show_item)

@bottle.route('/help')
def help():
  return static_file('help.html', root='/path/to/file')

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
  return bottle.redirect("/todo")

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

bottle.debug(True) #dev only, not for production
bottle.run(host='localhost', port=8082, reloader=True) #dev only
