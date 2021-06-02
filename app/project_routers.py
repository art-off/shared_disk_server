from . import app, db

from flask import request, make_response
from datetime import datetime

from .auth_utils import token_auth, get_token

from .models import Project, Task, Worker, Customer, Manager, DevelopmentStage, DevelopmentStageType
from .google_drive.utils import create_folder


@app.route('/project/start', methods=['POST'])
@token_auth.login_required
def start_project():
    token = get_token(request)

    name = request.json.get('name')
    customer_id = request.json.get('customer_id')
    manager_id = request.json.get('manager_id')
    deadline = request.json.get('deadline')

    project = Project(name=name,
                      deadline= datetime.strptime(deadline, '%Y-%m-%d'),
                      start_date=datetime.date(datetime.now()),
                      customer=Customer.query.get(customer_id),
                      manager=Manager.query.get(manager_id))

    error, project_folder_id = create_folder(token, "root", project.name)

    project.folder_id = project_folder_id
    db.session.add(project)

    for stage_json in request.json.get('stages'):
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
            task.folder_id = task_folder_id
            db.session.add(task)

    db.session.commit()

    return make_response({'status': 'fine'}, 200)
