import io, base64
import json
from typing import Annotated, Optional, List
import magic
from fastapi import Depends, HTTPException, UploadFile, Form, APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import gen_models
import models
import schema
from database import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()


def get_model(api_name):
    if api_name[-6:] != "_media":
        raise HTTPException(status_code=404, detail=f"{api_name} is not a media table")
    model_name = "".join([i.capitalize() for i in api_name.split("_")])
    if hasattr(gen_models, model_name):
        return getattr(gen_models, model_name)
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find table for {api_name}")


def get_model_v2(api_name):
    tbl = f"{api_name}_media"
    capitalized_words = [word.capitalize() for word in tbl.split('_')]
    # Join the words back together without spaces
    api_name = ''.join(capitalized_words)
    model_name = api_name

    if hasattr(gen_models, model_name):
        return getattr(gen_models, model_name)
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find table for {api_name}")


def check_parent(api_name, parent, db):
    table_name = api_name[:-6]
    table_model = "".join([i.capitalize() for i in table_name.split("_")])
    if hasattr(gen_models, table_model):
        table = getattr(gen_models, table_model)
        obj = db.query(table).filter(table.psk_id == parent).first()
        if obj:
            return True
        else:
            raise HTTPException(status_code=404, detail=f"Unable to find the parent at this id: {parent}")
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find  parent table for {api_name}")


@router.post('/crudapp/create/media/{api_name}', tags=['Media Model Creation'])
def enable_media_table(api_name: str, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.table_name == api_name).first()
    if not table:
        raise HTTPException(status_code=404, detail="Unable to find table")
    else:
        table.has_media = True
        db.commit()
        db.refresh(table)
        return table


@router.post('/crudapp/upload/media/{api_name}', tags=['Media Model Creation'])
async def upload_media_file(
        api_name: str,
        media: UploadFile,
        parent_psk_id: Annotated[Optional[int], Form()] = None,
        db: Session = Depends(get_db)
):
    model = get_model(api_name)
    contents = await media.read()
    mime = magic.Magic(mime=True)
    media_type = mime.from_buffer(contents)
    obj = model(
        file_blob=contents,
        file_mime=media_type,
        file_name=media.filename,
    )
    print(api_name)
    if parent_psk_id and check_parent(api_name, parent_psk_id, db):
        obj.parent_psk_id = parent_psk_id
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return {
            "psk_id": obj.psk_id,
            "filename": media.filename,
            "mime_type": media_type,
            "message": "file saved"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.put('/crudapp/upload/media/{api_name}/{psk_id}', tags=['Media Model Creation'])
async def update_media_file(
        api_name: str,
        psk_id: int,
        media: UploadFile,
        parent_psk_id: Annotated[Optional[int], Form()] = None,
        db: Session = Depends(get_db)
):
    model = get_model(api_name)

    # Find the existing media record by psk_id
    obj = db.query(model).filter(model.psk_id == psk_id).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Media file not found")

    # Read the new media contents
    contents = await media.read()
    mime = magic.Magic(mime=True)
    media_type = mime.from_buffer(contents)

    # Update the media file details
    obj.file_blob = contents
    obj.file_mime = media_type
    obj.file_name = media.filename

    if parent_psk_id and check_parent(api_name, parent_psk_id, db):
        obj.parent_psk_id = parent_psk_id

    try:
        db.commit()
        db.refresh(obj)
        return {
            "psk_id": obj.psk_id,
            "filename": media.filename,
            "mime_type": media_type,
            "message": "file updated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/crudapp/update/media_content', tags=['Media Model Creation'])
def media_content_update(request: schema.MediaContentSchema, db: Session = Depends(get_db)):
    api_name = request.api_name
    psk_id = request.psk_id

    model = get_model(api_name)

    # Find the existing media record by psk_id
    obj = db.query(model).filter(model.psk_id == psk_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"Media file record '{psk_id}' not found")

    obj.attachment_content = json.dumps(request.attachment_content)
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return {"message": "successfully updated content"}


@router.get('/crudapp/get/media/all/{api_name}', tags=['Media Model Creation'], response_model=List[schema.MediaSchema])
def get_all_media_data(api_name: str, db: Session = Depends(get_db)):
    model = get_model(api_name)
    medias = db.query(model).all()
    return medias


@router.get('/crudapp/get/media/{api_name}/parent/{parent_psk_id}', tags=['Media Model Creation'],
            response_model=List[schema.MediaSchema])
def get_media_by_parent(api_name: str, parent_psk_id: int, db: Session = Depends(get_db)):
    model = get_model(api_name)
    if not parent_psk_id:
        parent_psk_id = None
    medias = db.query(model).filter(model.parent_psk_id == parent_psk_id).all()
    return medias


@router.get('/crudapp/get/media/{api_name}/{psk_id}', tags=['Media Model Creation'], response_model=schema.MediaSchema)
def get_media_by_psk_id(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    model = get_model(api_name)
    medias = db.query(model).filter(model.psk_id == psk_id).first()
    if medias:
        return medias
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find data for id: {psk_id}")


@router.get('/crudapp/view/media/{api_name}/{psk_id}', tags=['Media Model Creation'])
def get_media_file(
        api_name: str,
        psk_id: int,
        download: Optional[bool] = False,
        db: Session = Depends(get_db)
):
    model = get_model(api_name)
    obj = db.query(model).filter(model.psk_id == psk_id).first()
    if obj:
        dis_type = "inline"
        if download:
            dis_type = "attachment"
        headers = {"Content-Disposition": f'{dis_type}; filename="{obj.file_name}"'}
        return StreamingResponse(io.BytesIO(obj.file_blob), media_type=obj.file_mime, headers=headers)
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find file for id: {psk_id}")


# ------------------------------------------  version 2 -------------------------------------------------------
# @router.get('/crudapp/view/media/v2/{api_name}/{psk_id}/{attachment_content}', tags=['Media Model Creation Version2'])
# def get_media_file(
#         api_name: str,
#         psk_id: int,
#         attachment_content: str,
#         download: Optional[bool] = False,
#         db: Session = Depends(get_db)
# ):
#     model = get_model(api_name)
#     obj = db.query(model).filter(model.psk_id == psk_id).first()
#
#     if not obj:
#         raise HTTPException(status_code=404, detail=f"Unable to find file for id: {psk_id}")
#
#     if obj.attachment_content != attachment_content:
#         raise HTTPException(status_code=404, detail=f"Attachment content mismatch for id: {psk_id}")
#
#     dis_type = "inline"
#     if download:
#         dis_type = "attachment"
#
#     headers = {"Content-Disposition": f'{dis_type}; filename="{obj.file_name}"'}
#     return StreamingResponse(io.BytesIO(obj.file_blob), media_type=obj.file_mime, headers=headers)


@router.get('/crudapp/view/media/v2/{table_uid}/{psk_id}', tags=['Media Model Creation Version2'])
def get_media_file(
        table_uid: str,
        psk_id: int,
        download: Optional[bool] = False,
        db: Session = Depends(get_db)
):
    tbl_obj = db.query(models.Table).filter(models.Table.uid == table_uid).first()

    if not tbl_obj:
        raise HTTPException(404, detail=f"Unable to find table uid: {table_uid}")

    api_name = tbl_obj.table_name

    model = get_model_v2(api_name)
    obj = db.query(model).filter(model.psk_id == psk_id).first()

    if not obj:
        raise HTTPException(status_code=404, detail=f"Unable to find file for id: {psk_id}")

    dis_type = "inline"
    if download:
        dis_type = "attachment"

    headers = {"Content-Disposition": f'{dis_type}; filename="{obj.file_name}"'}
    return StreamingResponse(io.BytesIO(obj.file_blob), media_type=obj.file_mime, headers=headers)


@router.post('/crudapp/upload/media/v2/{table_uid}', tags=['Media Model Creation Version2'])
async def upload_media_file(
        table_uid: str,
        media: UploadFile,
        parent_psk_id: Annotated[Optional[int], Form()] = None,
        db: Session = Depends(get_db)
):
    tbl_obj = db.query(models.Table).filter(models.Table.uid == table_uid).first()
    if not tbl_obj:
        raise HTTPException(404, detail=f"Unable to find table uid: {table_uid}")

    api_name = tbl_obj.table_name

    model = get_model_v2(api_name)

    # model = get_model(api_name)
    contents = await media.read()
    mime = magic.Magic(mime=True)
    media_type = mime.from_buffer(contents)
    obj = model(
        file_blob=contents,
        file_mime=media_type,
        file_name=media.filename,
    )

    table_name = f"{api_name}_media"
    if parent_psk_id and check_parent(table_name, parent_psk_id, db):
        obj.parent_psk_id = parent_psk_id
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return {
            "psk_id": obj.psk_id,
            "filename": media.filename,
            "mime_type": media_type,
            "message": "file saved"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.put('/crudapp/upload/media/v2/{table_uid}/{psk_id}', tags=['Media Model Creation Version2'])
async def update_media_file(
        table_uid: str,
        psk_id: int,
        media: UploadFile,
        parent_psk_id: Annotated[Optional[int], Form()] = None,
        db: Session = Depends(get_db)
):
    tbl_obj = db.query(models.Table).filter(models.Table.uid == table_uid).first()

    if not tbl_obj:
        raise HTTPException(404, detail=f"Unable to find table uid: {table_uid}")

    api_name = tbl_obj.table_name

    model = get_model_v2(api_name)

    # Find the existing media record by psk_id
    obj = db.query(model).filter(model.psk_id == psk_id).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Media file not found")

    # Read the new media contents
    contents = await media.read()
    mime = magic.Magic(mime=True)
    media_type = mime.from_buffer(contents)

    # Update the media file details
    obj.file_blob = contents
    obj.file_mime = media_type
    obj.file_name = media.filename
    # obj.attachment_content = attachment_content

    table_name = f"{api_name}_media"
    if parent_psk_id and check_parent(table_name, parent_psk_id, db):
        obj.parent_psk_id = parent_psk_id

    try:
        db.commit()
        db.refresh(obj)
        return {
            "psk_id": obj.psk_id,
            "filename": media.filename,
            "mime_type": media_type,
            "message": "file updated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.put('/crudapp/upload/media/v2/{table_uid}/{psk_id}', tags=['Media Model Creation Version2'])
# async def update_media_file(
#         request: schema.NewTestSchema,
#         table_uid: str,
#         psk_id: int,
#         media: UploadFile,
#         parent_psk_id: Annotated[Optional[int], Form()] = None,
#         db: Session = Depends(get_db)
# ):
#     print(request)
#     print(request.firstname)
#     return {"message": "Media file updated successfully"}


@router.delete('/crudapp/delete/media/v2/{api_name}/{psk_id}', tags=['Media Model Creation Version2'])
def delete_media_records(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    try:
        model_name = "".join([i.capitalize() for i in api_name.split("_")])
        if hasattr(gen_models, model_name):
            delete_model = getattr(gen_models, model_name)
            record = db.query(delete_model).filter(
                delete_model.psk_id == psk_id).first()
            if record:
                db.delete(record)
                db.commit()
            else:
                raise HTTPException(status_code=404, detail="Not Found")
            return {
                "message": f"Deleted [{psk_id}]"
            }
        else:
            raise HTTPException(
                status_code=404, detail=f"Unable to find table for {api_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.delete('/crudapp/delete_all_media_records/v2/{api_name}/{parent_psk_id}', tags=['Media Model Creation Version2'])
def delete_all_media_records(api_name: str, parent_psk_id: int, db: Session = Depends(get_db)):
    try:
        # Convert api_name to model name
        model_name = "".join([i.capitalize() for i in api_name.split("_")])

        # Check if the model exists in gen_models
        if hasattr(gen_models, model_name):
            delete_model = getattr(gen_models, model_name)

            # Fetch records to delete
            records = db.query(delete_model).filter(
                delete_model.parent_psk_id == parent_psk_id
            )

            if records.count() > 0:
                # Delete all records
                records.delete(synchronize_session=False)
                db.commit()
                return {"detail": f"All records for {api_name} with parent_psk_id {parent_psk_id} have been deleted successfully."}
            else:
                return {"detail": f"No records found for {api_name} with parent_psk_id {parent_psk_id}."}
        else:
            raise HTTPException(
                status_code=404, detail=f"Unable to find table for {api_name}"
            )
    except Exception as e:
        db.rollback()  # Rollback any changes in case of an error
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/crudapp/get/media_all_fields/v2/{api_name}/{psk_id}', tags=['Media Model Creation Version2'])
def get_media_by_psk_id(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    model = get_model(api_name)
    medias = db.query(model).filter(model.psk_id == psk_id).first()
    if medias:
        serialized_data = jsonable_encoder(medias, exclude={"file_blob"})
        return serialized_data
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find data for id: {psk_id}")