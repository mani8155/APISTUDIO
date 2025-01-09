def custom_api(db, models, data):
    try:
        user_id = int(data['user_id'])
    except KeyError:
        raise Exception("Missing key user_id")
    
    user = db.query(models.Asa02040101).filter(models.Asa02040101.psk_id == user_id).first()

    if user:
        return user.__dict__
    else:
        raise Exception("Not Found")
