#line 52
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError

import models
from models import AuthTokenGenerator, AuthTokenGeneratorMigrations, AuthTokenGeneratorLog
import schemas
from database import get_db
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Base.metadata.create_all(bind=engine)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
app = FastAPI(docs_url='/auth', openapi_url='/auth/openapi.json', title="Authentication API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    # print("fjshfjkshf")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:
        raise credentials_exception
    return payload


def create_auth_log(table_id, log, db):
    auth_log = AuthTokenGeneratorLog(
        table_id=table_id,
        created_date=datetime.utcnow(),
        log=log
    )
    db.add(auth_log)
    db.commit()
    db.refresh(auth_log)
    
# error fix the function 

@app.post('/auth/token', response_model=schemas.Token)
async def login_for_access_token(request: schemas.GenerateToken, db: Session = Depends(get_db)):
    print("function working")
    auth_data = db.query(AuthTokenGenerator).filter(AuthTokenGenerator.secret_key == request.secret_key).first()
    if not auth_data.active:
        raise HTTPException(status_code=401, detail="API Stopped")
    if not auth_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if auth_data.expiry_period == "never":
        pass
    elif auth_data.expiry_datetime < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Secret Key has expired")
    encodes = {"uid": auth_data.uid, "api_source": auth_data.api_source, "psk_uid": auth_data.psk_uid}
    expiry = datetime.utcnow() + timedelta(minutes=15)
    encodes['exp'] = expiry
    token = jwt.encode(encodes, SECRET_KEY, algorithm=ALGORITHM)
    create_auth_log(auth_data.id, f'New token generated for {auth_data.uid}', db)
    return schemas.Token(access_token=token, token_type='bearer')


def auth_migration(auth_data, db):
    auth_mig = AuthTokenGeneratorMigrations(
        table_id=auth_data.id,
        psk_uid=auth_data.psk_uid,
        uid=auth_data.uid,
        api_source=auth_data.api_source,
        secret_key=auth_data.secret_key,
        expiry_duration=auth_data.expiry_duration,
        expiry_period=auth_data.expiry_period,
        expiry_datetime=auth_data.expiry_datetime,
    )
    db.add(auth_mig)
    db.commit()
    db.refresh(auth_mig)


@app.post('/auth/create/authentication', response_model=schemas.AuthToken)
def create_authentication(form_data: schemas.AuthTokenCreate, db: Session = Depends(get_db)):
    try:
        auth_data = AuthTokenGenerator(**form_data.model_dump())
        auth_data.api_source = auth_data.api_source.name
        auth_data.expiry_period = auth_data.expiry_period.name
        auth_data.expiry_datetime = datetime.now()
        if auth_data.expiry_period != 'never':
            expiry_dataset = {
                "minutes": {"minutes": 1 * auth_data.expiry_duration},
                "hours": {"hours": 1 * auth_data.expiry_duration},
                "days": {"days": 1 * auth_data.expiry_duration},
                "months": {"days": 30 * auth_data.expiry_duration},
                "years": {"days": 365 * auth_data.expiry_duration},
            }
            expires = timedelta(**expiry_dataset[auth_data.expiry_period])
            expiry = datetime.utcnow() + expires
            auth_data.expiry_datetime = expiry
        db.add(auth_data)
        db.commit()
        db.refresh(auth_data)
        auth_migration(auth_data, db)
        create_auth_log(auth_data.id, f'New Secret Key Created for {auth_data.uid}', db)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="UID must be unique")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return auth_data


@app.get("/auth/api/details/", response_model=schemas.AuthPayload)
def get_auth_data(token: Annotated[schemas.AuthPayload, Depends(validate_token)]):
    return token


@app.get("/auth/api/tokens/")
def get_all_auth_tokens(db: Session = Depends(get_db)):
    auths = db.query(AuthTokenGenerator).all()
    return auths


# -------------------------------------------------------------------------------------------------------
@app.post("/auth/api/v1/run_stop/{id}")
def run_stop(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.AuthTokenGenerator).filter(models.AuthTokenGenerator.id == id).first()
    if obj.active:
        obj.active = False
        db.add(obj)
        db.commit()
        db.refresh(obj)

    else:
        obj.active = True
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj


