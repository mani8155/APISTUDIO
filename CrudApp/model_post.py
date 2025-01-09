from fastapi import Depends, FastAPI, HTTPException, UploadFile, Form, APIRouter
from database import get_db
from sqlalchemy.orm import Session
import models
import gen_models
import importlib
import schema
import os
from typing import Annotated, Optional, List
import magic
from fastapi.responses import StreamingResponse
import io


router = APIRouter()


def get_post_model(api_name):
    if api_name[-5:] == "_post":
        pass
    elif api_name[-14:] == "_post_reaction":
        pass
    else:
        raise HTTPException(status_code=404, detail=f"{api_name} is not a post table")
    model_name = "".join([i.capitalize() for i in api_name.split("_")])
    if hasattr(gen_models, model_name):
        return getattr(gen_models, model_name)
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find table for {api_name}")
    

def check_post_parent(table_name, parent, db):
    table_model = "".join([i.capitalize() for i in table_name.split("_")])
    if hasattr(gen_models, table_model):
        table = getattr(gen_models, table_model)
        obj = db.query(table).filter(table.psk_id==parent).first()
        if obj:
            return True
        else:
            raise HTTPException(status_code=404, detail=f"Unable to find the parent at this id: {parent}")
    else:
        raise HTTPException(status_code=404, detail=f"Unable to find  parent table")


@router.post('/crudapp/enable/post/{api_name}', tags=['Post Model Creation'])
def enable_post_table(api_name: str, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.table_name == api_name).first()
    if not table:
        raise HTTPException(status_code=404, detail="Unable to find table")
    else:
        table.has_posts = True
        db.commit()
        db.refresh(table)
        return table


@router.post('/crudapp/create/post/{api_name}', tags=['Post Model Creation'], response_model=schema.PostSchema)
def create_post(api_name: str, post: schema.PostCreateSchema, db: Session = Depends(get_db)):
    post_model = get_post_model(api_name)
    obj = post_model(post_comment=post.post_comment)

    if post.parent_psk_id and check_post_parent(api_name[:-5], post.parent_psk_id, db):
        obj.parent_psk_id = post.parent_psk_id

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.post('/crudapp/upload/post/{api_name}', tags=['Post Model Creation'])
async def upload_post(
        api_name: str, media: UploadFile,
        parent_psk_id: Optional[str] = None,
        db: Session = Depends(get_db)
):
    model = get_post_model(api_name)
    contents = await media.read()
    mime = magic.Magic(mime=True)
    media_type = mime.from_buffer(contents)
    obj = model(
        file_blob=contents,
        file_mime=media_type,
        file_name=media.filename,
    )
    if parent_psk_id and check_post_parent(api_name[:-5], parent_psk_id, db):
        obj.parent_psk_id = parent_psk_id
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return {
            "psk_id": obj.psk_id,
            "filename": media.filename,
            "mime_type": media_type,
            "message": "post saved"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get('/crudapp/get/post/all/{api_name}', tags=['Post Model Creation'], response_model=List[schema.PostSchema])
def get_all_posts(api_name: str, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    posts = db.query(model).all()
    return posts


@router.get('/crudapp/get/post/{api_name}/parent/{parent_psk_id}', tags=['Post Model Creation'], response_model=List[schema.PostSchema])
def get_post_by_parent(api_name: str, parent_psk_id: int, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    if not parent_psk_id:
        parent_psk_id = None
    posts = db.query(model).filter(model.parent_psk_id==parent_psk_id).all()
    return posts


@router.get('/crudapp/get/post/{api_name}/{psk_id}', tags=['Post Model Creation'], response_model=schema.PostSchema)
def get_post_by_psk_id(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    posts = db.query(model).filter(model.psk_id==psk_id).first()
    if not posts:
        raise HTTPException(status_code=404, detail=f"Unable to find post for id: {psk_id}")
    return posts


@router.put('/crudapp/update/post/{api_name}/{psk_id}', tags=['Post Model Creation'], response_model=schema.PostSchema)
def update_post(api_name: str, psk_id: int, post: schema.PostCreateSchema, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    posts = db.query(model).filter(model.psk_id==psk_id).first()
    if not posts:
        raise HTTPException(status_code=404, detail=f"Unable to find post for id: {psk_id}")
    posts.post_comment = post.post_comment
    db.commit()
    db.refresh(posts)
    return posts


@router.delete('/crudapp/delete/post/{api_name}/{psk_id}', tags=['Post Model Creation'])
def delete_post(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    posts = db.query(model).filter(model.psk_id==psk_id).first()
    if not posts:
        raise HTTPException(status_code=404, detail=f"Unable to find post for id: {psk_id}")
    db.delete(posts)
    db.commit()
    return {"message": "Deleted Post"}


@router.post('/crudapp/create/reaction/{api_name}', tags=['Post Reaction Creation'], response_model=schema.PostReactionSchema)
def create_reaction(api_name: str, reaction: schema.PostReactionCreateSchema, db: Session = Depends(get_db)):
    reaction_model = get_post_model(api_name)
    obj = reaction_model(reaction=reaction.reaction)

    if reaction.parent_psk_id and check_post_parent(api_name[:-14], reaction.parent_psk_id, db):
        obj.parent_psk_id = reaction.parent_psk_id

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.get('/crudapp/get/reaction/all/{api_name}', tags=['Post Reaction Creation'], response_model=List[schema.PostReactionSchema])
def get_all_reactions(api_name: str, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    reaction = db.query(model).all()
    return reaction


@router.get('/crudapp/get/reaction/{api_name}/parent/{parent_psk_id}', tags=['Post Reaction Creation'], response_model=List[schema.PostReactionSchema])
def get_reaction_by_parent(api_name: str, parent_psk_id: int, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    if not parent_psk_id:
        parent_psk_id = None
    reaction = db.query(model).filter(model.parent_psk_id==parent_psk_id).all()
    return reaction


@router.get('/crudapp/get/reaction/{api_name}/{psk_id}', tags=['Post Reaction Creation'], response_model=schema.PostReactionSchema)
def get_reaction_by_psk_id(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    reaction = db.query(model).filter(model.psk_id==psk_id).first()
    if not reaction:
        raise HTTPException(status_code=404, detail=f"Unable to find reaction for id: {psk_id}")
    return reaction


@router.put('/crudapp/update/reaction/{api_name}/{psk_id}', tags=['Post Reaction Creation'], response_model=schema.PostReactionSchema)
def update_reaction(api_name: str, psk_id: int, reaction: schema.PostReactionCreateSchema, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    reactions = db.query(model).filter(model.psk_id==psk_id).first()
    if not reactions:
        raise HTTPException(status_code=404, detail=f"Unable to find reaction for id: {psk_id}")
    reactions.reaction = reaction.reaction
    db.commit()
    db.refresh(reactions)
    return reactions


@router.delete('/crudapp/delete/reaction/{api_name}/{psk_id}', tags=['Post Reaction Creation'])
def delete_reaction(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    model = get_post_model(api_name)
    reaction = db.query(model).filter(model.psk_id==psk_id).first()
    if not reaction:
        raise HTTPException(status_code=404, detail=f"Unable to find reaction for id: {psk_id}")
    db.delete(reaction)
    db.commit()
    return {"message": "Deleted Post"}
