# def custom_api(db,models,data):
#     try:
#          user_input = data['menuadmin']
#     except KeyError:
#         raise Exception("Missing menuadmin Id")
#
#     menus_table = db.query(models.Menus).filter(models.Menus.menuadmin == f'{user_input}').all()
#
#     response = []
#
#     for menu in menus_table:
#         response.append(
#             {
#                 "menuadmin": menu.menuadmin,
#                 "menuname": menu.menuname,
#                 "menutype": menu.menutype,
#                 "menuhref": menu.menuhref,
#                 "menuicon": menu.menuicon,
#                 "tcode": menu.tcode,
#                 "status": menu.status,
#                 "psk_id": menu.id,
#             }
#         )
#
#     return response


# ---------------------- live ---------------------


def custom_api(db,models,data):
    try:
         user_input = data['menuadmin']
    except KeyError:
        raise Exception("Missing menuadmin Id")

    menus_table = db.query(models.Menus).filter(models.Menus.menuadmin == f'{user_input}').all()

    response = []

    for menu in menus_table:
        response.append(
            {
                "menuadmin": menu.menuadmin,
                "menuname": menu.menuname,
                "menutype": menu.menutype,
                "menuhref": menu.menuhref,
                "menuicon": menu.menuicon,
                "tcode": menu.tcode,
                "status": menu.status,
                "psk_id": menu.psk_id,
            }
        )

    return response
