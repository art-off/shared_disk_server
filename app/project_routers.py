from . import app, db

from datetime import datetime

from flask import request, make_response
from datetime import datetime

from .auth_utils import token_auth, get_token

from .models import Project, Task, Worker, Customer, Manager, DevelopmentStage, DevelopmentStageType
from .google_drive.utils import create_folder, give_permissions


@app.route('/project/start', methods=['POST'])
@token_auth.login_required
def start_project():
    token = get_token(request)

    name = request.json.get('name')
    customer_id = request.json.get('customer_id')
    manager_id = request.json.get('manager_id')
    deadline = request.json.get('deadline')

    project = Project(name=name,
                      deadline=datetime.strptime(deadline, '%Y-%m-%d'),
                      start_date=datetime.date(datetime.now()),
                      customer=Customer.query.get(customer_id),
                      manager=Manager.query.get(manager_id))

    error, project_folder_id = create_folder(token, "root", project.name)
    error, customer_project_folder_id = create_folder(token, project_folder_id, 'customer')
    give_permissions(token, customer_project_folder_id, project.customer.email)

    project.folder_id = project_folder_id
    project.customer_folder_id = customer_project_folder_id
    db.session.add(project)

    stages_json = request.json.get('stages')

    # все работники нужны чтобы дать всем доступы к финальным папкам
    all_workers = []
    for stage_json in stages_json:
        for task_json in stage_json['tasks']:
            all_workers.append(Worker.query.get(task_json['worker_id']))

    for stage_json in stages_json:
        dev_type = DevelopmentStageType.query.get(stage_json['type'])
        stage = DevelopmentStage(project=project,
                                 development_stage_type=dev_type)

        error, stage_folder_id = create_folder(token, project_folder_id, dev_type.name)
        stage.folder_id = stage_folder_id
        db.session.add(stage)

        for task_json in stage_json['tasks']:
            task = Task(name=task_json['name'],
                        development_stage=stage,
                        worker=Worker.query.get(task_json['worker_id']))
            error, task_folder_id = create_folder(token, stage_folder_id, task.name)
            error, customer_task_folder_id = create_folder(token, task_folder_id, f'{task.name} customer')
            error, finally_task_folder_id = create_folder(token, task_folder_id, f'{task.name} finally')

            give_permissions(token, task_folder_id, task.worker.email)
            give_permissions(token, customer_task_folder_id, project.customer.email)
            for w in all_workers:
                print(w.email)
                print(give_permissions(token, finally_task_folder_id, w.email))

            task.folder_id = task_folder_id
            task.customer_folder_id = customer_task_folder_id
            task.finally_folder_id = finally_task_folder_id
            db.session.add(task)

    db.session.commit()

    return make_response({'status': 'fine'}, 200)


@app.route('/project/get')
@token_auth.login_required
def get_projects():
    token = get_token(request)

    user = __get_user(token)
    if type(user) == Manager:
        user_projects = Project.query.filter_by(manager=user).all()
        return make_response({'projects': projects_to_json(user_projects)}, 200)
    elif type(user) == Worker:
        tasks = Task.query.filter_by(worker=user).all()
        stages = [x.development_stage for x in tasks]
        projects = list(set([x.project for x in stages]))
        return make_response({'projects': projects_to_json(projects)}, 200)


def projects_to_json(projects):
    json = []

    for p in projects:
        json.append({
            'id': p.id,
            'name': p.name,
            'deadline': p.deadline.strftime("%Y-%m-%d"),
            'start_time': p.start_date.strftime("%Y-%m-%d"),
            'folder_id': p.folder_id,
            'customer': {
                'id': p.customer.id,
                'first_name': p.customer.first_name,
                'middle_name': p.customer.middle_name,
                'last_name': p.customer.last_name,
                'email': p.customer.email,
            },
            'manager': {
                'id': p.manager.id,
                'name': p.manager.name,
                'email': p.manager.email,
            },
            'stages': __get_stages(p.id),
        })

    return json


def __get_stages(project_id):
    stages = DevelopmentStage.query.filter_by(project=Project.query.get(project_id)).all()
    stages_json = []
    for stage in stages:
        stage_json = {
            'id': stage.id,
            'type': stage.development_stage_type.name,
            'folder_id': stage.folder_id,
            'tasks': []
        }
        tasks = Task.query.filter_by(development_stage=stage).all()
        for task in tasks:
            stage_json['tasks'].append({
                'id': task.id,
                'name': task.name,
                'ready': task.ready,
                'folder_id': task.folder_id,
                'customer_folder_id': task.customer_folder_id,
                'finally_folder_id': task.finally_folder_id,
                'worker': {
                    'id': task.worker.id,
                    'name': task.worker.name,
                    'email': task.worker.email,
                    'profession_type': task.worker.profession_type.id,
                }
            })
        stages_json.append(stage_json)

    return stages_json


def __get_user(token):
    user = Manager.query.filter_by(token=token).first()
    if user is None:
        user = Worker.query.filter_by(token=token).first()
    return user
