from flask import request, make_response

from app import app
from app.models import Project, Manager, Customer, CreateEditFileFolderTable, DevelopmentStage, Task, VisitFolderTable


@app.route('/web/auth', methods=['POST'])
def web_auth():
    email = request.json.get('email')
    password = request.json.get('password')

    print(request.json)

    if email is None or password is None:
        return make_response({'error': 'required params does not exist'}, 403)

    manager = Manager.query.filter_by(email=email).first()
    if manager is not None:
        return make_response({'id': manager.id, 'ismanager': True}, 200)

    customer = Customer.query.filter_by(email=email).first()
    if customer is not None:
        return make_response({'id': customer.id, 'ismanager': False}, 200)

    return make_response({}, 400)


@app.route('/web/projects', methods=['POST'])
def web_projects():
    user_id = request.json.get('id')
    is_manager = request.json.get('ismanager')

    projects = []
    if is_manager:
        projects = Project.query.filter_by(manager=Manager.query.get(user_id)).all()
        print(projects)
    else:
        projects = Project.query.filter_by(customer=Customer.query.get(user_id)).all()
        print(projects)

    json = []
    for p in projects:
        json.append({
            'id': p.id,
            'name': p.name,
            'customer': p.customer.email,
            'manager': p.manager.name,
        })

    return make_response({'projects': json}, 200)


@app.route('/web/create_or_edit_file_folder')
def web_create_or_edit_file_folder():
    project_id = int(request.json.get('project_id'))
    is_manager = request.json.get('ismanager')

    return make_response({'table': [
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
    ]}, 200)

    # stages = DevelopmentStage.query.filter_by(project=Project.query.get(project_id)).all()
    # tasks = []
    # for stage in stages:
    #     t = Task.query.filter_by(development_stage=stage).all()
    #     tasks += t
    #
    # file_folder_actions = []
    # for task in tasks:
    #     file_folder_actions += CreateEditFileFolderTable.query.filter_by(task_id=task.id)
    #
    # print(file_folder_actions)
    # return make_response({}, 200)


@app.route('/web/visit')
def web_visir():
    project_id = int(request.json.get('project_id'))
    is_manager = request.json.get('ismanager')

    return make_response({'table': [
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
        ['value1', 'value2', 'value3', 'value4', 'value5'],
    ]}, 200)

    # stages = DevelopmentStage.query.filter_by(project=Project.query.get(project_id)).all()
    # tasks = []
    # for stage in stages:
    #     t = Task.query.filter_by(development_stage=stage).all()
    #     tasks += t
    #
    # file_folder_actions = []
    # for task in tasks:
    #     file_folder_actions += VisitFolderTable.query.filter_by(task_id=task.id)
    #
    # print(file_folder_actions)
    # return make_response({}, 200)


@app.route('/web/used_disk_space')
def web_used_disk_space():
    project_id = int(request.json.get('project_id'))
    is_manager = request.json.get('ismanager')

    return make_response({
        'design': {
            'task1': '4 mb',
            'task2': '10 mb',
        },
        'develop': {
            'task3': '512 mb'
        },
        'testing': None,
    }, 200)


@app.route('/web/info_about_iterations')
def info_about_iterations():
    project_id = int(request.json.get('project_id'))
    is_manager = request.json.get('ismanager')

    return make_response({
        'design': None,
        'develop': {
            'task1': 0,
            'task2': 1,
        },
        'testing': {
            'task3': 2
        },
    }, 200)


@app.route('/web/diagram_of_stages')
def web_diagram_of_stages():
    project_id = int(request.json.get('project_id'))
    is_manager = request.json.get('ismanager')

    return make_response({
        'design': 3,
        'develop': 44,
        'testing': 0,
    }, 200)


@app.route('/web/diagrams_of_tasks')
def web_diagrams_of_tasks():
    project_id = int(request.json.get('project_id'))
    is_manager = request.json.get('ismanager')

    return make_response({
        'design': {
            'task1': 13,
            'task2': 4
        },
        'develop': {
            'task3': 33,
            'task4': 12
        },
        'testing': {
            'task5': 3,
            'task6': 12
        },
    }, 200)


@app.route('/web/links')
def web_links():
    project_id = int(request.json.get('project_id'))
    is_manager = request.json.get('ismanager')

    return make_response({
        'design': {
            'task1': 'https://drive.google.com/drive/folders/1FBIX3lPYgznq9b0vyChivk2uQDTraaR4?usp=sharing',
            'task2': 'https://drive.google.com/drive/folders/1FBIX3lPYgznq9b0vyChivk2uQDTraaR4?usp=sharing',
        },
        'develop': {
            'task3': 'https://drive.google.com/drive/folders/1FBIX3lPYgznq9b0vyChivk2uQDTraaR4?usp=sharing',
        },
        'testing': None,
    }, 200)
