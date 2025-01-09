import os
from alembic.config import Config
from alembic import command
import models
import gen_models
import typer
from database import engine, Base
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
import inspect

app = typer.Typer()

ALEMBIC_INI_PATH = os.path.join(os.getcwd(), 'alembic.ini')
ALEMBIC_CONFIG = Config(ALEMBIC_INI_PATH)


def migrate_db(msg):
    try:
        command.revision(ALEMBIC_CONFIG, autogenerate=True, message=msg)
        command.upgrade(ALEMBIC_CONFIG, "head")
        return {"code": 200, "message": "Migration complete"}
    except SQLAlchemyError as e:
        return {"code": 500, "message": e}


def swap_columns(model_name, col_1, col_2, custom=False):

    if hasattr(models, model_name):
        model = getattr(models, model_name)
    elif hasattr(gen_models, model_name):
        model = getattr(gen_models, model_name)
    else:
        return "Model not found"

    if not hasattr(model, col_1):
        return f"{col_1} not in model"

    if not hasattr(model, col_2):
        return f"{col_2} not in model"

    with Session(engine) as session:
        data_list = session.query(model).all()
        try:
            for data in data_list:
                data_col = getattr(data, col_1)
                query = {col_2: data_col}
                if not custom:
                    statement = update(model).where(
                        model.id == data.id).values(**query)
                else:
                    statement = update(model).where(
                        model.psk_id == data.psk_id).values(**query)

                session.execute(statement)
                session.commit()
            return "Updated Successfully"
        except Exception as e:
            return e


def get_table(table: int):
    with Session(engine) as session:
        table = session.query(models.Table).filter(
            models.Table.id == table).first()
        if table:
            try:
                session.delete(table)
                session.commit()
                return "Table Deleted"
            except Exception as e:
                return e
        else:
            return "Table not Found"


@app.command()
def migrate(message: str):
    result = migrate_db(message)
    print(result)


@app.command()
def swap_models(model_name: str, col_1: str, col_2: str, custom_models: bool = False):
    result = swap_columns(model_name, col_1, col_2, custom_models)
    print(result)


@app.command()
def delete_table(table_id: int):
    print(get_table(table_id))


@app.command()
def generate_psk_uid():
    with Session(engine) as session:
        tables = session.query(models.Table).all()
        for table in tables:
            if table.published:
                model_name = ''.join([i.capitalize()
                                     for i in table.table_name.split("_")])
                if hasattr(gen_models, model_name):
                    _model = getattr(gen_models, model_name)
                    _get_table_rows = session.query(_model).all()
                    count = 0
                    for _row in _get_table_rows:
                        if not _row.psk_uid:
                            _row.psk_uid = uuid4().__str__()
                            session.commit()
                            session.refresh(_row)
                            count += 1
                    print(f"{model_name}: Updated {count} rows")

        module_attrs = inspect.getmembers(models, inspect.isclass)
        models_list = [attr[1] for attr in module_attrs if isinstance(
            attr[1], type) and issubclass(attr[1], Base)]
        for model in models_list:
            if hasattr(model, 'psk_uid'):
                _model = session.query(model).all()
                count = 0
                for _row in _model:
                    if not _row.psk_uid:
                        _row.psk_uid = uuid4().__str__()
                        session.commit()
                        session.refresh(_row)
                        count += 1
                print(f"{model.__name__}: Updated {count} rows")


@app.command()
def generate_ids():
    with Session(engine) as session:
        tables = session.query(models.Table).all()
        for table in tables:
            if table.published:
                model_name = ''.join([i.capitalize()
                                     for i in table.table_name.split("_")])
                if hasattr(gen_models, model_name):
                    _model = getattr(gen_models, model_name)
                    _get_table_rows = session.query(_model).all()
                    count = 0
                    for _row in _get_table_rows:
                        _row.app_psk_id = _row.psk_id
                        _row.app_uid = _row.psk_uid
                        session.commit()
                        session.refresh(_row)
                        count += 1
                    print(f"{model_name}: Updated {count} rows")


@app.command()
def add_file_to_field():
    with Session(engine) as session:
        api_metas = session.query(models.ApiMeta).filter(
            models.ApiMeta.api_source == "custom").all()
        for api_meta in api_metas:
            try:
                file_path = os.path.join(
                    os.getcwd(), 'custom_apis', api_meta.code_name)

                with open(file_path, 'rb') as file:
                    binary_data = file.read()
                    api_meta.python_file = binary_data
                    session.commit()
                    session.refresh(api_meta)
            except Exception as e:
                pass


if __name__ == '__main__':
    app()
