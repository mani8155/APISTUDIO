def custom_api(db,models,data):
    try:
         user_input = data['menuadmin']
    except KeyError:
        raise Exception("Missing menuadmin Id")

    response = db.query(models.Menus).filter(models.Menus.menuadmin == f'{user_input}').all()
    return response
