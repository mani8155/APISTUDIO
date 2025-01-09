import json
import requests


def get_application_list(url):
    response = requests.get(url, data=json.dumps({'data': {}}), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.text)


def app_import(apps, parent_id, db, models):
    app_created = 0
    app_updated = 0
    for app in apps:
        _app = db.query(models.ApiStudioAppName).filter(models.ApiStudioAppName.app_id == app['app_id']).first()
        if not _app:
            _app = models.ApiStudioAppName(
                app_id=app['app_id'],
                api_studio_app_group_id=parent_id,
                name=app['name'],
                type=app['type']
            )
            db.add(_app)
            app_created += 1
        else:
            _app.name = app['name']
            _app.type = app['type']
            app_updated += 1
        db.commit()
        db.refresh(_app)
    return app_created, app_updated


def child_group_import(children, parent_id, db, models):
    child_created = 0
    app_created = 0
    app_updated = 0
    for child_group in children:
        _child = db.query(models.ApiStudioAppGroup).filter(
            models.ApiStudioAppGroup.group_id == child_group['group_id']).first()
        if not _child:
            _child = models.ApiStudioAppGroup(
                name=child_group['name'],
                group_id=child_group['group_id'],
                parent_id=parent_id,
                child=False,
            )
            db.add(_child)
            child_created += 1
        else:
            _child.name = child_group['name']
        db.commit()
        db.refresh(_child)

        _app_created, _app_updated = app_import(child_group['app_names'], _child.psk_id, db, models)
        app_created += _app_created
        app_updated += _app_updated

    return child_created, app_created, app_updated


def custom_api(db, models, data):
    parent_created = 0
    child_created = 0
    app_created = 0
    app_updated = 0
    try:
        url = data['url']
    except KeyError as e:
        raise Exception(e)
    app_group_list = get_application_list(url)
    for parent_group in app_group_list:
        _parent = db.query(models.ApiStudioAppGroup).filter(
            models.ApiStudioAppGroup.group_id == parent_group['group_id']).first()
        if not _parent:
            _parent = models.ApiStudioAppGroup(
                name=parent_group['name'],
                group_id=parent_group['group_id'],
                parent_id=0,
                child=True,
            )
            db.add(_parent)
            parent_created += 1
        else:
            _parent.name = parent_group['name']
        db.commit()
        db.refresh(_parent)

        _child_created, _app_created, _app_updated = child_group_import(parent_group['children'], _parent.psk_id, db, models)
        child_created += _child_created
        app_created += _app_created
        app_updated += _app_updated

    return {
        'parent_created': parent_created,
        'child_created': child_created,
        'app_created': app_created,
        'app_updated': app_updated
    }
