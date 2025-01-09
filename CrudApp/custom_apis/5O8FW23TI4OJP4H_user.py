# def custom_api(db,models, data):
#     users = db.query(models.Users).all()
#     role_privileges = db.query(models.Roleprivileges).all()
#     _list = []
#
#     for user in users:
#         for rp in role_privileges:
#             if int(user.role) == rp.id:
#
#                 _list.append({
#                     "user_role": int(user.role),
#                     "username": user.username,
#                     "rolepriv_id": rp.id,
#                     "rolename": rp.rolename
#                 })
#     return _list


# ------------------------------ live code ---------------------------------


def custom_api(db,models, data):
    users = db.query(models.Users).all()
    role_privileges = db.query(models.Roleprivileges).all()
    _list = []

    for user in users:
        for rp in role_privileges:
            if int(user.role) == rp.psk_id:

                _list.append({
                    "user_role": int(user.role),
                    "username": user.username,
                    "rolepriv_id": rp.psk_id,
                    "rolename": rp.rolename
                })
    return _list
