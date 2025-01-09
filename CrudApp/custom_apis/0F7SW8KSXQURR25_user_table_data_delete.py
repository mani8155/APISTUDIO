# def custom_api(db, models, data):
#     input_id = data['user_id']
#     user = db.query(models.Users).filter(models.Users.id == int(input_id)).first()
#     db.delete(user)
#     db.commit()
#
#     return {"message": "User deleted successfully"}


# ---------------------- live -------------------------]

def custom_api(db, models, data):
    input_id = data['user_id']
    user = db.query(models.Users).filter(models.Users.psk_id == int(input_id)).first()
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
