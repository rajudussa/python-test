
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# Example tasks
tasks = [
    {
        'id': 1,
        'title': u'Web application',
        'description': u'Create a simple web application',
        'done': False
    },
    {
        'id': 2,
        'title': u'Add database',
        'description': u'Add database to the website',
        'done': False
    }
]


#Get all tasks
@app.route('/tasks/', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


# Throws an error msg for valid formats
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid Request made Not found'}), 404)


# Get a task by id
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# Create a new task
@app.route('/tasks/', methods=['POST'])
def create_task():
    print(request.json)
    if not request.json or not 'title' in request.json:
        abort(404)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# Update a task by id
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# Delete a task by id
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

