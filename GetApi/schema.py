from pydantic import BaseModel
from typing import Dict, List
from enum import Enum


class QueryOperations(Enum):
    equal = "equal"
    not_equal = "not_equal"
    less_than = "less_than"
    greater_than = "greater_than"
    contains = "contains"
    order_asc = "order_asc"
    order_desc = "order_desc"


class QueryField(BaseModel):
    field: str
    value: str
    operation: QueryOperations


class SearchType(Enum):
    first = "first"
    all = "all"


class QuerySchema(BaseModel):
    queries: List[QueryField]
    search_type: SearchType
