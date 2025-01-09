def custom_api(db, models, data):
    try:
        table_name = "".join([i.capitalize() for i in data['tablename'].split("_")])
        field_name = data['fieldname']
        value = data['value']

        if hasattr(models, table_name):
            _model = getattr(models, table_name)
            if hasattr(_model, field_name):
                _model_with_field = getattr(_model, field_name)
                rp = db.query(_model).filter(_model_with_field == value).first()
                if rp:
                    return {"count": 1}
                else:
                    return {"count": 0}
            else:
                raise Exception(f"Unable to find {field_name} from table {data['tablename']}")
        else:
            raise Exception(f"Unable to find {data['tablename']}")
    except Exception as e:
        return {"detail": str(e)}





# def custom_api(db, models, data):
#     _table_name = data['tablename'].capitalize()
#     _field_name = data['fieldname']
#     value = data['value']
#
#     role_privileges = db.query(models._table_name).all()
#
#     for rp in role_privileges:
#         if value == rp._field_name:
#             data = {"row_cont": 1}
#             return data
#
#     else:
#         data = {"row_cont": 0}
#         return data



# --------------------------------- live code --------------------
#
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


