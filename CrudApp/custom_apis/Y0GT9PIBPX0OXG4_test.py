




# def custom_api(db, models, data):
#     role_privileges = db.query(models.Roleprivileges).all()
#     menus = db.query(models.Menus).all()
#     assign_priv = db.query(models.AssignmenuRoleprivilege).all()
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
#                                 if ap.roleid == str(user.role):
#
#                                     user_roles.append({
#                                             "username": user.username,
#                                             "userroleid": int(rolepri.id),
#                                             "id": int(rolepri.id),
#                                             "rolename": rolepri.rolename,
#                                             "rolecode": rolepri.rolecode,
#                                             "roleprivid": privilege_id,
#                                             "roleid": int(ap.roleid),
#                                             "menuid": int(ap.menuid),
#                                             "menuname": menu.menuname,
#                                             "menuicon": menu.menuicon,
#                                             "menutype": menu.menutype,
#                                             "tcode": menu.tcode,
#                                             "menuhref": menu.menuhref
#                                         })
#
#     return user_roles



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
        users = db.query(models.Users).filter(models.Users.role == str(rolepri.id)).all()

        # for user in users:
        privilege_names = [int(privilege_id) for privilege_id in rolepri.privilege_name.split(',')]
        for privilege_id in privilege_names:

            for rolepri in role_privileges:
                for menu in menus:
                    for ap in assign_priv:
                        if ap.roleid == str(rolepri.id) and ap.menuid == str(menu.id):

                            for user in users:
                                if ap.roleid == str(user.role) and user.username == username:

                                    user_roles.append({
                                            "username": user.username,
                                            "role": user.role,
                                            "id": int(rolepri.id),
                                            "rolename": rolepri.rolename,
                                            "rolecode": rolepri.rolecode,
                                            "roleprivid": privilege_id,
                                            "roleid": int(ap.roleid),
                                            "menuid": int(ap.menuid),
                                            "menuname": menu.menuname,
                                            "menuicon": menu.menuicon,
                                            "menutype": menu.menutype,
                                            "tcode": menu.tcode,
                                            "menuhref": menu.menuhref,
                                            "menu_seq": menu.menu_seq,

                                        })

    return user_roles