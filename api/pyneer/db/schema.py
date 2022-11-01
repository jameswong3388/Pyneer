"""
Schema is used to validate the data that is being passed to the database
"""


class Schema:
    def __init__(self, schemas):
        self.schema = schemas

    """
    Validate the data that is being passed to the database
    
    e.g 
    from api.pyneer.db.schema import schema

    model_schema = {
        "name": str,
        "age": int,
        "email": str,
        "password": int,
    }

    datas = {
        "name": 'John',
        "age": 20,
        "email": "email@localhost.com",
        "password": '1f'
    }
    
    print(schema(model_schema).validate(datas))
    """
    def validate(self, data):
        for key, value in self.schema.items():
            if key not in data:
                return {'valid': False, 'message': f'{key} is required'}
            if type(data[key]) != value:
                return {'valid': False, 'message': f'{key} must be {value}'}
        return {'valid': True}
