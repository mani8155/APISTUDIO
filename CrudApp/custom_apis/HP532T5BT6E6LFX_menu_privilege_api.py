def custom_api(db, models, data):
    try:
        user_id = int(data['user_id'])
    except KeyError:
        raise Exception("Missing key user_id")
    
    user = db.query(models.Asa02040101).filter(models.Asa02040101.psk_id == user_id).first()

    if user:
        menus = []
        user_group = user.user_groups
        menu_privs = db.query(models.Asa02030101).filter(models.Asa02030101.menu_group_name.icontains(user_group)).all()
        for mp in menu_privs:
            menus.append(mp.__dict__)
        return menus
    else:
        raise Exception("Not Found")
