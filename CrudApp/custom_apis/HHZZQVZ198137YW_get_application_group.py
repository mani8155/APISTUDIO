def custom_api(db, models, data):
    try:
        group_id = int(data['group_id'])
    except KeyError:
        raise Exception("Missing key group_id")
    
    a_group = db.query(models.ApiStudioAppGroup).filter(models.ApiStudioAppGroup.psk_id==group_id).first()
    if not a_group:
        raise Exception("Not Found")
    app_names = db.query(models.ApiStudioAppName).filter(models.ApiStudioAppName.api_studio_app_group_id==group_id).order_by(models.ApiStudioAppName.app_id).all()

    app_group = {
        "psk_id": a_group.psk_id,
        "name": a_group.name,
        "group_id": a_group.group_id,
        "applications": [{
            "psk_id": a_name.psk_id,
            "name": a_name.name,
            "app_id": a_name.app_id,
            "type": a_name.type,
            "api_studio_app_group_id": a_name.api_studio_app_group_id
        } for a_name in app_names]
    }

    return app_group
