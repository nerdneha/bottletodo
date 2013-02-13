import sqlite3
from bottle import route, run, debug, template, request, validate
from bottle import error, redirect


@route('/todo')
def todo_list():
  if request.GET.get('save','').strip():
    edit = request.GET.get('task','').strip()
    status = request.GET.get('status','').strip()
    no = request.GET.get('no','').strip()
    if status == 'open':
      status = 1
    else:
      status = 0
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE?", (edit,
                                                                      status,
                                                                      no))
    conn.commit()
    return redirect("/todo")
  else:
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    open_items = c.fetchall()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '0'")
    closed_items = c.fetchall()
    c.close()
    output = template('make_list', open_rows=open_items,
                      closed_rows=closed_items)
    return output

@route('/new', method='GET')
def new_item():
  if request.GET.get('save','').strip():
    new = request.GET.get('task', '').strip()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO todo (task, status) VALUES (?,?)", (new,1))
    new_id = c.lastrowid
    conn.commit()
    c.close()
    return '<p>The new task was inserted into the database, the ID is %s</p>' %new_id
  else:
    return template('new_task')

@route('/edit/:no', method='GET')
@validate(no=int)
def edit_item(no):
  if request.GET.get('save','').strip():
    edit = request.GET.get('task','').strip()
    status = request.GET.get('status','').strip()
    if status == 'open':
      status = 1
    else:
      status = 0
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE?", (edit,
                                                                      status,
                                                                      no))
    conn.commit()
    return '<p>The item number %s was successfully updated</p>' %no
  else:
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
    cur_data = c.fetchone()
    return template('edit_task', old=cur_data, no=no)

@route('/item:item#[1-9]+#')
def show_item(item):
  conn = sqlite3.connect('todo.db')
  c = conn.cursor()
  c.execute("SELECT task FROM todo WHERE id LIKE ?", (item))
  result = c.fetchall()
  c.close()
  if not result:
    return 'This item number does not exist!'
  else:
    return 'Task: %s' %result[0]

@route('/help')
def help():
  return static_file('help.html', root='/path/to/file')

@route('/json:json#[1-9]+#')
def show_json(json):
  conn = sqlite3.connect('todo.db')
  c = conn.cursor()
  c.execute("SELECT task FROM todo WHERE id LIKE ?", (json))
  result = c.fetchall()
  c.close()
  if not result:
    return {'task':'This item number does not exist!'}
  else:
    return {'Task': result[0]}

@error(404)
def mistake404(code):
  return 'Sorry, this page does not exist!'

@error(403)
def mistake403(code):
  return 'The parameter you passed has the wrong format!'

debug(True) #dev only, not for production
run(reloader=True) #dev only
