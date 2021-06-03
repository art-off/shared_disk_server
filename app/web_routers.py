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

    stages = DevelopmentStage.query.filter_by(project=Project.query.get(project_id)).all()
    tasks = []
    for stage in stages:
        t = Task.query.filter_by(development_stage=stage).all()
        tasks += t

    file_folder_actions = []
    for task in tasks:
        file_folder_actions += CreateEditFileFolderTable.query.filter_by(task_id=task.id)

    print(file_folder_actions)
    return make_response({}, 200)


@app.route('/web/visit')
def web_visir():
    project_id = int(request.json.get('project_id'))

    stages = DevelopmentStage.query.filter_by(project=Project.query.get(project_id)).all()
    tasks = []
    for stage in stages:
        t = Task.query.filter_by(development_stage=stage).all()
        tasks += t

    file_folder_actions = []
    for task in tasks:
        file_folder_actions += VisitFolderTable.query.filter_by(task_id=task.id)

    print(file_folder_actions)
    return make_response({}, 200)