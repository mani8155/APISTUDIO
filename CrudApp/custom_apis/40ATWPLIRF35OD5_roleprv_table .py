def custom_api(db, models, data):

    _input = {
        "tablename": data['tablename'].capitalize(),
        "fieldname": data['fieldname'],
        "value": data['value']
    }


    #
    # role_privileges = db.query(models.Roleprivileges).all()
    #
    # for rp in role_privileges:
    #     if _input == rp.rolename:
    #         data = {"row_cont": int(1)}
    #         return data
    #
    # else:
    #     data = {"row_cont": int(0)}
    #     return data

    return _input['tablename']


# --------------------------------- live code --------------------

# def custom_api(db, models, data):
#     _input = data['rolename']
#     role_privileges = db.query(models.Roleprivileges).all()
#
#     for rp in role_privileges:
#         if _input == rp.rolename:
#             data = {"row_cont": int(1)}
#             return data
#
#     else:
#         data = {"row_cont": int(0)}
#         return data
#
#
