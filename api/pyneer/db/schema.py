"""
Schema is used to validate the data that is being passed to the database.
"""


class schema:
    def __init__(self, schemas):
        self.schema = schemas

    def validate(self, data):
        for key, value in self.schema.items():
            if key not in data:
                return {'valid': False, 'message': f'{key} is required'}
            if type(data[key]) != value:
                return {'valid': False, 'message': f'{key} must be {value}'}
        return {'valid': True}
