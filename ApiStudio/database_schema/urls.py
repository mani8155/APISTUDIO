from django.urls import path, include
from . views import *

urlpatterns = [
    path('schemas/', schemas, name="schemas"),
    path('schemas/<int:id>/', schemas_list, name="schemas_list"),
    path('add_schema/<int:id>/', add_new_schema, name="add_schema"),
    path('table_list/<int:id>/<str:schema_name>/', table_list, name="table_list"),
    path('column_list/<int:id>/<str:schema_name>/<str:table_name>/', column_list, name="column_list"),
    path('field_property_view/<int:id>/<str:schema_name>/<str:table_name>/<field_name>/', field_property_view,
         name="field_property_view"),
    path('get_records/<int:id>/<str:schema_name>/<str:table_name>/', get_records, name="get_records"),

    path('permision_schema/<int:id>/<str:connection>/', permision_schema, name="permision_schema"),


    # ------------------- sql ------------

    path('sql_tables/<int:id>/', sql_tables_list, name="sql_tables"),
    path('sql_columns/<int:id>/<str:table_name>/', mysql_column_list, name="sql_columns"),
    path('sql_table_records/<int:id>/<str:table_name>/', mysql_get_records, name="sql_table_records"),

    # ------------- mssql -------------------

    path('mssql_tables/<int:id>/', mssql_tables_list, name="mssql_tables_list"),
    path('mssql_columns/<int:id>/<str:table_name>/', mssql_column_list, name="mssql_column_list"),
    path('mssql_get_records/<int:id>/<str:table_name>/', mssql_get_records, name="mssql_get_records"),


]
