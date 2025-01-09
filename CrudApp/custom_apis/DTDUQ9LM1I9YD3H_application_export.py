def app_names(db, group_id, models):
    return [{
        "name": app_name.name,
        "app_id": app_name.app_id,
        "type": app_name.type,
    } for app_name in db.query(models.ApiStudioAppName).filter(
        models.ApiStudioAppName.api_studio_app_group_id == group_id).all()]


def group_children(db, group_id, models):
    return [{
        "name": app_group.name,
        "group_id": app_group.group_id,
        "app_names": app_names(db, app_group.psk_id, models)
    } for app_group in db.query(models.ApiStudioAppGroup).filter(models.ApiStudioAppGroup.parent_id == group_id).all()]


def custom_api(db, models, data):
    app_groups = db.query(models.ApiStudioAppGroup).all()
    app_group_list = []
    for app_group in app_groups:
        if app_group.child:
            _app_group = {
                "name": app_group.name,
                "group_id": app_group.group_id,
                "children": group_children(db, app_group.psk_id, models)
            }

            app_group_list.append(_app_group)

    return app_group_list

