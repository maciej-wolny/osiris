import datetime

from google.cloud.bigquery import SchemaField
from google.cloud.exceptions import NotFound

FIELD_TYPE = {
    str: 'STRING',
    bytes: 'BYTES',
    int: 'INTEGER',
    float: 'FLOAT',
    bool: 'BOOLEAN',
    datetime.datetime: 'DATETIME',
    datetime.date: 'DATE',
    datetime.time: 'TIME',
    dict: 'RECORD',
}


def map_dict_to_bq_schema(source_dict):
    """Maps dictionary data type into BigQuery schema. Useful in development and testing."""
    schema = []
    if source_dict is None:
        return None
    for key, value in source_dict.items():
        try:
            schema_field = SchemaField(key, FIELD_TYPE[type(value)])
        except KeyError:
            if value and len(value) > 0:
                schema_field = SchemaField(key,
                                           FIELD_TYPE[type(value[0])],
                                           mode='REPEATED')
        schema.append(schema_field)
        if schema_field.field_type == 'RECORD':
            schema_field._fields = map_dict_to_bq_schema(value)
    return schema


def table_exist(client, table_ref):
    """Checks if BigQuery table exists."""
    try:
        client.get_table(table_ref)
        return True
    except NotFound:
        return False
