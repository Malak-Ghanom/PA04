from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import marshal


app = Flask(__name__)

# index variable for tasks list
index_lists = 1
# index variable for tasks
index_tasks = 1
# index variable for remove and edit list
index = 1

# lists variable
task_list = {}
tasks_list = {}
task_list['tasks']=[]

# tasks variable
task = {}
tasks = {}


# save data
# store = marshal.dumps(task_list)
# store = marshal.dumps( tasks_list)
# store=marshal.dumps(task)
# store=marshal.dumps(tasks)
# store=marshal.dumps(index)
# store=marshal.dumps(index_lists)
# store=marshal.dumps(index_tasks)

# load=marshal.loads(task_list)
# load=marshal.loads(tasks_list)
# load=marshal.loads(tasks)
# load=marshal.loads(task)
# load=marshal.loads(index_lists)
# load=marshal.loads(index)
# load=marshal.loads(index_tasks)

# login templates
@ app.route('/')
def login():
    return render_template('login.html')

# base of the all pages
@ app.route('/base')
def base():
    return render_template('base.html')

# home page that contain existing lists
@ app.route('/home')
def home():
    return render_template('home.html', tasks_list=tasks_list, tasks=tasks)

# create a new list
@ app.route('/newlist', methods=['POST', 'GET'])
def new_list():
    global index_lists
    if request.method == 'GET':
        return render_template('new-list.html')
    else:
        time=datetime.now()
        list_name=request.form['list_name']
        task_list['name']=list_name
        task_list['created_at']=time
        print(time)
        tasks_list[index_lists]=task_list.copy()
        index_lists += 1
        return redirect('home')

# add new task
@ app.route('/newtask', methods=['POST', 'GET'])
def new_task():
    global index_tasks,tasks_list
    if request.method == 'GET':
        return render_template('new-task.html',tasks_list=tasks_list)
    else:
        time=datetime.now()
        task_name=request.form['task_name']
        status = request.form['status']
        priority = request.form['priority']
        description = request.form['description']
        assigned_list = request.form['assigned_list']

        task['name']=task_name
        task['created_at']=time
        task['status']=status
        task['priority']=priority
        task['description']=description
        tasks[index_tasks]=task.copy()
        index_tasks += 1
        
        for tasklist in tasks_list.values():
            if tasklist['name'] == assigned_list:
                tasklist['tasks'].append(task.copy())

        return redirect(url_for('home'))

# view details for a given list
@ app.route('/list/view/<int:index>')
def view_list(index):
    view_list=tasks_list[index]
    return render_template('view-list.html', view_list=view_list)

# remove specific list
@ app.route('/list/remove/<int:index>')
def remove_list(index):
    global tasks_list
    del tasks_list[index]
    return render_template('home.html', tasks_list=tasks_list, tasks=tasks)


# edit name of the list
@ app.route('/list/edit/<int:index>', methods=['GET', 'POST'])
def edit_list(index):
    if request.method == 'GET':
        view_list=tasks_list[index]
        return render_template('edit-list.html', view_list=view_list)
    else:
        name=request.form['new_name']
        tasks_list[index]['name']=name
        return redirect(url_for('home'))
