# def custom_api(db, models, data):
#     try:
#         username = data['username']
#     except KeyError:
#         raise Exception("Missing key username")
#
#     role_privileges = db.query(models.Roleprivileges).all()
#     menus = db.query(models.Menus).all()
#     assign_priv = db.query(models.AssignmenuRoleprivilege).all()
#
#     user_roles = []
#
#     for rolepri in role_privileges:
#         users = db.query(models.Users).filter(models.Users.role == str(rolepri.id)).all()
#
#         # for user in users:
#         privilege_names = [int(privilege_id) for privilege_id in rolepri.privilege_name.split(',')]
#         for privilege_id in privilege_names:
#
#             for rolepri in role_privileges:
#                 for menu in menus:
#                     for ap in assign_priv:
#                         if ap.roleid == str(rolepri.id) and ap.menuid == str(menu.id):
#
#                             for user in users:
#                                 if ap.roleid != str(user.role) and user.username == username:
#
#                                     user_roles.append({
#                                             "username": user.username,
#                                             "menuid": int(ap.menuid),
#                                             "menuname": menu.menuname
#
#
#                                         })
#
#     return user_roles




# ------------------------------ live code ---------------------------------


def custom_api(db, models, data):
    try:
        username = data['username']
    except KeyError:
        raise Exception("Missing key username")

    role_privileges = db.query(models.Roleprivileges).all()
    menus = db.query(models.Menus).all()
    assign_priv = db.query(models.AssignmenuRoleprivilege).all()

    user_roles = []

    for rolepri in role_privileges:
        users = db.query(models.Users).filter(models.Users.role == str(rolepri.psk_id)).all()

        # for user in users:
        privilege_names = [int(privilege_id) for privilege_id in rolepri.privilege_name.split(',')]
        for privilege_id in privilege_names:

            for rolepri in role_privileges:
                for menu in menus:
                    for ap in assign_priv:
                        if ap.roleid == str(rolepri.psk_id) and ap.menuid == str(menu.psk_id):

                            for user in users:
                                if ap.roleid != str(user.role) and user.username == username:

                                    user_roles.append({
                                            "username": user.username,
                                            "menuid": int(ap.menuid),
                                            "menuname": menu.menuname


                                        })

    return user_roles
