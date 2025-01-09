def custom_api(db, models, data):
    try:
        user_input = data['username']
    except KeyError:
        raise Exception("Missing username Id")

    user = db.query(models.Gmc12020101).filter(models.Gmc12020101.username == user_input).first()

    role_pri = db.query(models.Roleprivileges).all()

    user_role = user.role

    for role in role_pri:
        if int(user_role) == role.psk_id:
            response = {
                "psk_id": int(user.psk_id),
                "username": user.username,
                "password": user.password,
                "rolename": role.rolename,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "mobile_no": user.mobileno,
                "email_id": user.emailid,
                "status": user.status
            }

            return response
