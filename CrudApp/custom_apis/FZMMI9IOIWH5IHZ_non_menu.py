# def custom_api(db, models, data):
#     try:
#          user_input = data['role_id']
#     except KeyError:
#         raise Exception("Missing Role Id")
#
#     role_privileges = db.query(models.Roleprivileges).all()
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
#             if ap.roleid != str(rolepri.id):
#                 menu = db.query(models.Menus).filter(models.Menus.id == int(ap.menuid)).first()
#                 role_p['menus'].append({
#                     "menuid": int(ap.menuid),
#                     "menuname": menu.menuname
#                 })
#         user_roles.append(role_p)
#
#     # Filter user_roles list to include only the role with role_id equal to 5
#     filtered_user_roles = [role for role in user_roles if role['role_id'] == user_input]
#
#     filtered_user_roles1 = filtered_user_roles[0]['menus'] if filtered_user_roles else []
#
#     return filtered_user_roles1






# ------------------------------ live code ---------------------------------

# def custom_api(db, models, data):
#     try:
#          user_input = data['role_id']
#     except KeyError:
#         raise Exception("Missing Role Id")
#
#     role_privileges = db.query(models.Roleprivileges).all()
#     assign_priv = db.query(models.AssignmenuRoleprivilege).all()
#
#     user_roles = []
#
#     for rolepri in role_privileges:
#         role_p = {
#             "role_id": rolepri.psk_id,
#             "rolename": rolepri.rolename,
#             "menus": []
#         }
#         for ap in assign_priv:
#             if ap.roleid != str(rolepri.psk_id):
#                 menu = db.query(models.Menus).filter(models.Menus.psk_id == int(ap.menuid)).first()
#                 role_p['menus'].append({
#                     "menuid": int(ap.menuid),
#                     "menuname": menu.menuname
#                 })
#         user_roles.append(role_p)
#
#     # Filter user_roles list to include only the role with role_id equal to 5
#     filtered_user_roles = [role for role in user_roles if role['role_id'] == user_input]
#
#     return filtered_user_roles


def custom_api(db, models, data):
    try:
         user_input = data['role_id']
    except KeyError:
        raise Exception("Missing Role Id")

    role_privileges = db.query(models.Roleprivileges).all()
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
                menu = db.query(models.Menus).filter(models.Menus.psk_id == int(ap.menuid)).first()
                role_p['menus'].append({
                    "menuid": int(ap.menuid),
                    "menuname": menu.menuname
                })
        user_roles.append(role_p)

    # Filter user_roles list to include only the role with role_id equal to 5
    filtered_user_roles = [role for role in user_roles if role['role_id'] == user_input]

    filtered_user_roles1 = filtered_user_roles[0]['menus'] if filtered_user_roles else []

    return filtered_user_roles1