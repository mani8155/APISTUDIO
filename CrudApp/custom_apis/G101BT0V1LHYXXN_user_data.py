# def custom_api(db, models, data):
#     try:
#         user_input = data['username']
#     except KeyError:
#         raise Exception("Missing username Id")
#
#     user = db.query(models.Users).filter(models.Users.username == user_input).first()
#
#     role_pri = db.query(models.Roleprivileges).all()
#
#     user_role = user.role
#
#     response = []
#
#     for role in role_pri:
#         if int(user_role) == role.id:
#             response.append(
#                 {
#                     "psk_id": int(user.id),
#                     "username": user.username,
#                     "password": user.password,
#                     "rolename": role.rolename,
#                     "firstname": user.firstname,
#                     "lastname": user.lastname,
#                     "mobile_no": user.mobileno,
#                     "email_id": user.emailid,
#                     "status": user.status
#                 }
#             )
#
#             return response





# ------------------------------ live code ---------------------------------


def custom_api(db, models, data):
    try:
        user_input = data['username']
    except KeyError:
        raise Exception("Missing username Id")

    user = db.query(models.Users).filter(models.Users.username == user_input).first()

    role_pri = db.query(models.Roleprivileges).all()

    user_role = user.role

    response = []

    for role in role_pri:
        if int(user_role) == role.psk_id:
            response.append(
                {
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
            )

            return response
