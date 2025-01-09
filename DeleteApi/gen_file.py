import json


def get_default_columns():
    cols = "    transaction_id = Column(Integer)\n"
    cols += "    transaction_remarks = Column(Text)\n"
    cols += "    api_id = Column(String)\n"
    cols += "    app_psk_id = Column(Integer)\n"
    cols += "    app_uid = Column(String)\n"
    cols += "    psk_uid = Column(String, default=uuid.uuid4)\n"
    cols += "    user_id = Column(Integer)\n"
    cols += "    created_by = Column(String)\n"
    cols += "    created_on = Column(DateTime, default=func.now())\n"
    cols += "    updated_by = Column(String)\n"
    cols += "    updated_on = Column(DateTime, onupdate=func.now())\n"
    cols += "    cancel_by = Column(String)\n"
    cols += "    cancel_on = Column(DateTime)\n"
    cols += "    cancel_status = Column(String)\n"
    cols += "    cancel_remarks = Column(String)\n"
    cols += "    approval_level_1 = Column(Integer)\n"
    cols += "    approval_level_2 = Column(Integer)\n"
    cols += "    approval_remarks = Column(Integer)\n"
    cols += "    workflow_id = Column(String)\n"
    cols += "    workflow_role = Column(String)\n"
    cols += "    row_order = Column(Integer)\n"
    cols += "    gis_latitude = Column(Float)\n"
    cols += "    gis_longitude = Column(Float)\n"
    cols += "    cdn_location = Column(String)\n"
    return cols


def get_media_code(table_name, model_name):
    media_model = f"class {model_name}Media(Base):\n"
    media_model += f'    __tablename__ = "{table_name}_media"\n\n'
    media_model += f"    psk_id = Column(Integer, primary_key=True, index=True)\n"
    media_model += f"    psk_uid = Column(String, default=uuid.uuid4)\n"
    media_model += f"    parent_psk_id = Column(Integer, ForeignKey('{table_name}.psk_id'))\n"
    media_model += f"    {table_name} = relationship('{model_name}', back_populates='{table_name}_media')\n"
    media_model += f"    app_id = Column(String)\n"
    media_model += f"    user_id = Column(String)\n"
    media_model += f"    row_order = Column(Integer)\n"
    media_model += f"    created_by = Column(String)\n"
    media_model += f"    created_on = Column(DateTime, default=func.now())\n"
    media_model += f"    updated_by = Column(String)\n"
    media_model += f"    updated_on = Column(DateTime, default=func.now())\n"
    media_model += f"    cancel_by = Column(String)\n"
    media_model += f"    cancel_on = Column(DateTime)\n"
    media_model += f"    cancel_status = Column(String)\n"
    media_model += f"    cancel_remarks = Column(String)\n"
    media_model += f"    attachment_content = Column(Text)\n"
    media_model += f"    file_blob = Column(LargeBinary)\n"
    media_model += f"    file_mime = Column(String)\n"
    media_model += f"    file_name = Column(String)\n"
    media_model += f"    file_path = Column(String)\n"
    media_model += f"    gis_latitude = Column(Float)\n"
    media_model += f"    gis_longitude = Column(Float)\n"

    return media_model


def get_post_code(table_name, model_name):
    post_model = f"class {model_name}Post(Base):\n"
    post_model += f'    __tablename__ = "{table_name}_post"\n\n'
    post_model += f"    psk_id = Column(Integer, primary_key=True, index=True)\n"
    post_model += f"    psk_uid = Column(String, default=uuid.uuid4)\n"
    post_model += f"    parent_psk_id = Column(Integer, ForeignKey('{table_name}.psk_id'))\n"
    post_model += f"    {table_name} = relationship('{model_name}', back_populates='{table_name}_post')\n"
    post_model += f"    post_reaction = relationship('{model_name}PostReaction', back_populates='post')\n"
    post_model += f"    app_id = Column(String)\n"
    post_model += f"    user_id = Column(String)\n"
    post_model += f"    row_order = Column(Integer)\n"
    post_model += f"    post_comment = Column(String)\n"
    post_model += f"    created_by = Column(String)\n"
    post_model += f"    created_on = Column(DateTime, default=func.now())\n"
    post_model += f"    updated_by = Column(String)\n"
    post_model += f"    updated_on = Column(DateTime, default=func.now())\n"
    post_model += f"    cancel_by = Column(String)\n"
    post_model += f"    cancel_on = Column(DateTime)\n"
    post_model += f"    cancel_status = Column(String)\n"
    post_model += f"    cancel_remarks = Column(String)\n"
    post_model += f"    file_blob = Column(LargeBinary)\n"
    post_model += f"    file_mime = Column(String)\n"
    post_model += f"    file_name = Column(String)\n"
    post_model += f"    file_path = Column(String)\n"
    post_model += f"    gis_latitude = Column(Float)\n"
    post_model += f"    gis_longitude = Column(Float)\n\n\n"

    post_model += f"class {model_name}PostReaction(Base):\n"
    post_model += f'    __tablename__ = "{table_name}_post_reaction"\n\n'
    post_model += f"    psk_id = Column(Integer, primary_key=True, index=True)\n"
    post_model += f"    psk_uid = Column(String, default=uuid.uuid4)\n"
    post_model += f"    parent_psk_id = Column(Integer, ForeignKey('{table_name}.psk_id'))\n"
    post_model += f"    {table_name} = relationship('{model_name}', back_populates='{table_name}_post_reaction')\n"
    post_model += f"    post_psk_id = Column(Integer, ForeignKey('{table_name}_post.psk_id'))\n"
    post_model += f"    post = relationship('{model_name}Post', back_populates='post_reaction')\n"
    post_model += f"    app_id = Column(String)\n"
    post_model += f"    user_id = Column(String)\n"
    post_model += f"    row_order = Column(Integer)\n"
    post_model += f"    reaction = Column(String)\n"
    post_model += f"    created_by = Column(String)\n"
    post_model += f"    created_on = Column(DateTime, default=func.now())\n"
    post_model += f"    updated_by = Column(String)\n"
    post_model += f"    updated_on = Column(DateTime, default=func.now())\n"
    post_model += f"    cancel_by = Column(String)\n"
    post_model += f"    cancel_on = Column(DateTime)\n"
    post_model += f"    cancel_status = Column(String)\n"
    post_model += f"    cancel_remarks = Column(String)\n"
    post_model += f"    gis_latitude = Column(Float)\n"
    post_model += f"    gis_longitude = Column(Float)\n\n\n"

    return post_model


def check_constraints(field_property):
    constraint = ''

    if field_property.get('basic'):
        prop = field_property['basic']

        # Check if 'unique' is set to True
        if prop.get("unique"):
            constraint += ', unique=True'

        # If 'nullable' is False, set nullable=False, otherwise default to nullable=True
        if prop.get("nullable", True) is False:
            constraint += ', nullable=False'
        else:
            constraint += ', nullable=True'

    return constraint



def generate_models(tables_data):
    models_code = ""

    for table in tables_data:
        table_name = ''.join([i.capitalize() for i in table.table_name.split("_")])
        class_definition = f"class {table_name}(Base):\n"
        class_definition += f'    __tablename__ = "{table.table_name}"\n\n'
        class_definition += f'    psk_id = Column(Integer, primary_key=True, index=True)\n'
        class_definition += get_default_columns()

        class_attrs = []
        validators = ""
        for field in table.fields:
            field_name = field.field_name
            field_type = field.field_data_type
            try:
                field_property = json.loads(field.field_property)
            except Exception as e:
                field_property = {}

            if field_type == "integer":
                class_attrs.append(f"    {field_name} = Column(Integer{check_constraints(field_property)})")
            elif field_type == "float":
                class_attrs.append(f"    {field_name} = Column(Float{check_constraints(field_property)})")
            elif field_type == "string":
                class_attrs.append(f"    {field_name} = Column(String{check_constraints(field_property)})")
            elif field_type == "boolean":
                class_attrs.append(f"    {field_name} = Column(Boolean)")
            elif field_type == "date":
                class_attrs.append(f"    {field_name} = Column(Date{check_constraints(field_property)})")
                validators += f"    @validates('{field_name}')\n"
                validators += f"    def validate_{field_name}(self, key, {field_name}):\n"
                validators += f"        if not rule_engine.is_valid_date({field_name}, ('%d-%m-%Y', '%Y-%m-%d')):\n"
                validators += f'            raise ValueError(f"Invalid date format: {{{field_name}}}. Valid Format is DD-MM-YYYY or YYYY-MM-DD")\n'
                validators += f'        return {field_name}\n\n'
            elif field_type == "time":
                class_attrs.append(f"    {field_name} = Column(Time{check_constraints(field_property)})")
                validators += f"    @validates('{field_name}')\n"
                validators += f"    def validate_{field_name}(self, key, {field_name}):\n"
                validators += f"        if not rule_engine.is_valid_date({field_name}, '%H:%M:%S'):\n"
                validators += f'            raise ValueError(f"Invalid time format: {{{field_name}}}. Valid Format is HH:MM:SS and must be in range 00:00:00 - 23:59:59")\n'
                validators += f'        return {field_name}\n\n'
            elif field_type == "email":
                class_attrs.append(f"    {field_name} = Column(String{check_constraints(field_property)})")
                validators += f"    @validates('{field_name}')\n"
                validators += f"    def validate_{field_name}(self, key, {field_name}):\n"
                validators += f"        if not rule_engine.is_valid_email({field_name}):\n"
                validators += f'            raise ValueError(f"Invalid email address: {{{field_name}}}")\n'
                validators += f'        return {field_name}\n\n'
            elif field_type == "password":
                class_attrs.append(f"    {field_name} = Column(String{check_constraints(field_property)})")
            elif field_type == "text":
                class_attrs.append(f"    {field_name} = Column(Text{check_constraints(field_property)})")
            elif field_type == "single_select":
                class_attrs.append(f"    {field_name} = Column(Text{check_constraints(field_property)})")
            elif field_type == "multi_select":
                class_attrs.append(f"    {field_name} = Column(Text{check_constraints(field_property)})")
            elif field_type == "grid":
                class_attrs.append(f"    {field_name} = Column(Text{check_constraints(field_property)})")
            elif field_type == "foreign_key":
                related_table_name = field.related_to
                class_attrs.append(f"    {field_name} = Column(Integer, ForeignKey('{related_table_name}.psk_id'))")

        media_code = ""
        posts_code = ""
        if table.has_media:
            class_attrs.append(f"    {table.table_name}_media = relationship('{table_name}Media', back_populates='{table.table_name}', cascade='all, delete-orphan')")
            media_code = get_media_code(table.table_name, table_name) + "\n\n"
        if table.has_posts:
            class_attrs.append(f"    {table.table_name}_post = relationship('{table_name}Post', back_populates='{table.table_name}', cascade='all, delete-orphan')")
            class_attrs.append(f"    {table.table_name}_post_reaction = relationship('{table_name}PostReaction', back_populates='{table.table_name}', cascade='all, delete-orphan')")
            posts_code = get_post_code(table.table_name, table_name) + "\n\n"

        class_definition += "\n".join(class_attrs)
        class_definition += f"\n\n{validators}"
        models_code += class_definition + "\n\n"
        models_code += media_code
        models_code += posts_code

    with open('gen_models.py', 'w') as model_file:
        model_file.write("from sqlalchemy import (create_engine, Column, Date, DateTime,\n")
        model_file.write("                        Integer, String, Boolean, ForeignKey,\n")
        model_file.write("                        Float, func, Time, LargeBinary, Text)\n")
        model_file.write("from database import Base\n")
        model_file.write("from sqlalchemy.orm import relationship\n")
        model_file.write("import rule_engine\n")
        model_file.write("import datetime\n")
        model_file.write("import uuid\n")
        model_file.write("from sqlalchemy.orm import validates\n")
        model_file.write("from sqlalchemy.orm import relationship\n\n\n")
        model_file.write("class ApiSysConfig(Base):\n")
        model_file.write('    __tablename__ = "api_sys_config"\n\n')
        model_file.write("    id = Column(Integer, primary_key=True, index=True, unique=True)\n")
        model_file.write("    config_name = Column(String)\n\n\n")
        model_file.write("# ----- GENERATED MODELS -----\n")
        model_file.write(models_code)
