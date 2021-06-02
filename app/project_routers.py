from . import app, db

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
