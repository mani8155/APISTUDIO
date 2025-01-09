def custom_api(db, models, data):
    try:
        group_id = int(data['group_id'])
    except KeyError:
        raise Exception("Missing key group_id")
    
    a_group = db.query(models.ApiStudioAppGroup).filter(models.ApiStudioAppGroup.psk_id==group_id).first()
    if not a_group:
        raise Exception("Not Found")
    app_names = db.query(models.ApiStudioAppName).filter(models.ApiStudioAppName.api_studio_app_group_id==group_id).order_by(models.ApiStudioAppName.app_id).all()

    for app in app_names:
        if app:
            db.delete(app)
            db.commit()

    db.delete(a_group)
    db.commit()

    return "Deleted Successfully"
