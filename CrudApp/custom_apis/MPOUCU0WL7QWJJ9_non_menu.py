# def custom_api(db, models, data):
#     role_privileges = db.query(models.Roleprivileges).all()
#     # menus = db.query(models.Menus).all()
#     assign_priv = db.query(models.AssignmenuRoleprivilege).all()
#
#     user_roles = []
#
#     for rolepri in role_privileges:
#         for ap in assign_priv:
#             if ap.roleid != str(rolepri.id):
#                 menu = db.query(models.Menus).filter(models.Menus.id == int(ap.menuid)).first()
#                 user_roles.append({
#                         "role_id": rolepri.id,
#                         "rolename": rolepri.rolename,
#                         "menuid": int(ap.menuid),
#                         "menuname": menu.menuname
#                     })
#
#     return user_roles


# def custom_api(db, models, data):
#     role_privileges = db.query(models.Roleprivileges).all()
#     # menus = db.query(models.Menus).all()
#     assign_priv = db.query(models.AssignmenuRoleprivilege).all()
#
#     user_roles = []
#
#     for rolepri in role_privileges:
#         role_p = {
#             "role_id": rolepri.id,
#             "rolename": rolepri.rolename,
#             "menus": []
#         }
#         for ap in assign_priv:
#
#             if ap.roleid != str(rolepri.id):
#                 menu = db.query(models.Menus).filter(models.Menus.id==int(ap.menuid)).first()
#                 role_p['menus'].append({
#                         "menuid": int(ap.menuid),
#                         "menuname": menu.menuname
#                     })
#         user_roles.append(role_p)
#     return user_roles


# ------------------------------ live code ---------------------------------


def custom_api(db, models, data):
    role_privileges = db.query(models.Roleprivileges).all()
    # menus = db.query(models.Menus).all()
    assign_priv = db.query(models.AssignmenuRoleprivilege).all()

    user_roles = []

    for rolepri in role_privileges:
        role_p = {
            "role_id": rolepri.psk_id,
            "rolename": rolepri.rolename,
            "menus": []
        }
        for ap in assign_priv:

            if ap.roleid != str(rolepri.psk_id):
                menu = db.query(models.Menus).filter(models.Menus.psk_id==int(ap.menuid)).first()
                role_p['menus'].append({
                        "menuid": int(ap.menuid),
                        "menuname": menu.menuname
                    })
        user_roles.append(role_p)
    return user_roles
