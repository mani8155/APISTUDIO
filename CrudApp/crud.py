from fastapi import Depends, FastAPI, HTTPException, UploadFile, Form, APIRouter
from database import get_db
from sqlalchemy.orm import Session
import models
import gen_models
import importlib
import schema
import os

router = APIRouter()


@router.get("/crudapp/api/{uid}/", tags=['Custom Api Usage'])
async def custom_get_api(uid: str, data: schema.CRUDSchema, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.uid == uid).first()
    if api_meta.api_method not in ["get"]:
        raise HTTPException(status_code=405, detail="Method not allowed")
    if api_meta.api_source == "custom":
        response_data = None
        module_name = api_meta.code_name.replace(".py", "")

        try:
            file_path = os.path.join(os.getcwd(), 'custom_apis', f'{module_name}.py')
            module_spec = importlib.util.spec_from_file_location(module_name, file_path)
            custom_api = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(custom_api)
            if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
                response_data = custom_api.custom_api(db, gen_models, data.data)
                return response_data
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")


@router.post("/crudapp/api/{uid}/", tags=['Custom Api Usage'])
async def custom_post_api(uid: str, data: schema.CRUDSchema, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.uid == uid).first()
    if api_meta.api_method not in ["post"]:
        raise HTTPException(status_code=405, detail="Method not allowed")
    if api_meta.api_source == "custom":
        response_data = None
        module_name = api_meta.code_name.replace(".py", "")
        try:
            file_path = os.path.join(os.getcwd(), 'custom_apis', f'{module_name}.py')
            module_spec = importlib.util.spec_from_file_location(module_name, file_path)
            custom_api = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(custom_api)
            if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
                response_data = custom_api.custom_api(db, gen_models, data.data)
                return response_data
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")


@router.put("/crudapp/api/{uid}/", tags=['Custom Api Usage'])
async def custom_put_api(uid: str, data: schema.CRUDSchema, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.uid == uid).first()
    if api_meta.api_method not in ["put"]:
        raise HTTPException(status_code=405, detail="Method not allowed")
    if api_meta.api_source == "custom":
        response_data = None
        module_name = api_meta.code_name.replace(".py", "")
        try:
            file_path = os.path.join(os.getcwd(), 'custom_apis', f'{module_name}.py')
            module_spec = importlib.util.spec_from_file_location(module_name, file_path)
            custom_api = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(custom_api)
            if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
                response_data = custom_api.custom_api(db, gen_models, data.data)
                return response_data
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")


@router.delete("/crudapp/api/{uid}/", tags=['Custom Api Usage'])
async def custom_delete_api(uid: str, data: schema.CRUDSchema, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.uid == uid).first()
    if api_meta.api_method not in ["delete"]:
        raise HTTPException(status_code=405, detail="Method not allowed")
    if api_meta.api_source == "custom":
        response_data = None
        module_name = api_meta.code_name.replace(".py", "")
        try:
            file_path = os.path.join(os.getcwd(), 'custom_apis', f'{module_name}.py')
            module_spec = importlib.util.spec_from_file_location(module_name, file_path)
            custom_api = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(custom_api)
            if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
                response_data = custom_api.custom_api(db, gen_models, data.data)
                return response_data
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")
