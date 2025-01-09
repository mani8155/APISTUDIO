# def custom_api(db, models, data):
#     role_privileges = db.query(models.Roleprivileges).all()
#     role_table = db.query(models.Roles).all()
#     _list = []
#
#     for role in role_table:
#         for rp in role_privileges:
#             if role.id == int(rp.privilege_name):
#
#                 _list.append({
#                     "role_id": role.id,
#                     "rp_name": rp.privilege_name,
#                     "role_rolename": role.rolename,
#                     "rp_rolename": rp.rolename,
#                 })
#
#     return _list

#

# ------------------------------ live code ---------------------------------


def custom_api(db, models, data):
    role_privileges = db.query(models.Roleprivileges).all()
    role_table = db.query(models.Roles).all()
    _list = []

    for role in role_table:
        for rp in role_privileges:
            if role.psk_id == int(rp.privilege_name):

                _list.append({
                    "role_id": role.psk_id,
                    "rp_name": rp.privilege_name,
                    "role_rolename": role.rolename,
                    "rp_rolename": rp.rolename,
                })

    return _list