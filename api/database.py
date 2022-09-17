from api import crud


def query(key, value, table, file='databases/database.json'):
    """
    This function will query the databases.json file and return a result
    with all the data that matches the key and value.

    (:param) key: Dictionary key
    (:param) value: Dictionary value
    (:param) table: Table's name

    if nothing is found, it will return an empty list, []
    """

    read_data = crud.read(file=file, table=table, queried_key=[])

    if read_data['status'] and read_data['result']:

        new_result = []

        for data in read_data['result']:
            try:
                if data[key] == value:
                    new_dict = data
                    new_result.append(new_dict)

            except KeyError:
                return {'status': False, 'message': 'Key does not exist.'}

        return {'status': True, 'message': "", 'result': new_result}

    else:
        return {'status': False, 'message': 'No data found'}


def generate_new_id(table, file='databases/database.json'):
    """
    This function will get the last id of the table and add 1 to it.

    (:param) table: The table name
    """

    read_data = crud.read(file=file, table=table, queried_key=['id'])

    if read_data['status'] and read_data['result']:
        new_id = read_data['result'][-1]['id'] + 1
        return {'status': True, 'message': "", 'result': new_id}

    else:
        return {'status': False, 'message': 'No data found'}
