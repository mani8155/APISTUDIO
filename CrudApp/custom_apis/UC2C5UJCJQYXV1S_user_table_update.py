# def custom_api(db, models, data):
#     try:
#         _input_id = data['user_id']
#         _input_username = data['username']
#         _input_email = data['email']
#         _input_mobile = data['mobile_number']
#
#         user = db.query(models.Users).filter(models.Users.id == _input_id).first()
#
#         if user:
#             if user.username != _input_username:
#                 user.username = _input_username
#             if user.emailid != _input_email:
#                 user.emailid = _input_email
#             if user.mobileno != _input_mobile:
#                 user.mobileno = _input_mobile
#
#             db.commit()
#
#             response_data = {"status": "success", "message": "profile updated successfully "}
#             return response_data
#         else:
#             raise Exception("User not found")
#
#
#     except Exception as e:
#         return {"detail": str(e)}
#


# -------------------- live ---------------------


def custom_api(db, models, data):
    try:
        _input_id = data['user_id']
        _input_username = data['username']
        _input_email = data['email']
        _input_mobile = data['mobile_number']

        user = db.query(models.Users).filter(models.Users.psk_id == _input_id).first()

        if user:
            if user.username != _input_username:
                user.username = _input_username
            if user.emailid != _input_email:
                user.emailid = _input_email
            if user.mobileno != _input_mobile:
                user.mobileno = _input_mobile

            db.commit()

            response_data = {"status": "success", "message": "profile updated successfully "}
            return response_data
        else:
            raise Exception("User not found")


    except Exception as e:
        return {"detail": str(e)}

