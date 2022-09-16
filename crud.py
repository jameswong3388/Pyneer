import json


def create(file, mode, table, data):
    try:
        f = open(file, mode)
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": e, "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": e, "status": False}

    except Exception as e:
        return {"message": e, "status": False}

    else:
        if table in loaded_data and data != {} and isinstance(data, dict):
            loaded_data[table].append(data)

            f.seek(0)
            json.dump(loaded_data, f, indent=2)

            f.close()

            return {"message": "Successful . . .", "status": True}
        else:
            return {"message": "Failed . . .", "status": False}


def read(file, mode, table, queried_key):
    # queried_key is a list of keys to be queried from the table e.g. ['username', 'password', 'role']

    new_lists = []

    try:
        f = open(file, mode)
        loaded_data = json.loads(f.read())

    except FileNotFoundError as e:
        return {"message": e, "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": e, "status": False}

    except Exception as e:
        return {"message": e, "status": False}

    else:
        if table in loaded_data and queried_key != [] and isinstance(queried_key, list):

            for i in loaded_data[table]:
                new_dict = {}

                for key in queried_key:
                    if key in i and key != '':
                        new_dict[key] = i[key]
                    else:
                        return {"message": "Key not found . . .", "status": False}

                new_lists.append(new_dict)

            f.close()
            return {"message": "Successfully . . . ", "status": True, "result": new_lists}

        elif table in loaded_data and queried_key == []:
            return {"message": "Successfully . . . ", "status": True, "result": loaded_data[table]}

        else:
            return {"message": "Failed . . .", "status": False, "result": []}


def update(file, mode, table, data):

    # data is a dictionary with the following keys:
    # unique_key, unique_value, key, value

    try:
        f = open(file, mode)
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": e, "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": e, "status": False}

    except Exception as e:
        return {"message": e, "status": False}

    else:
        if table in loaded_data and data != {} and isinstance(data, dict) and data['unique_key'] != '' and data['unique_value'] != '':
            for i in loaded_data[table]:
                if i[data['unique_key']] == data['unique_value']:

                    print('yes')
                    try:
                        i[data['key']] = data['value']

                    except KeyError as e:
                        return {"message": e, "status": False}


            f.seek(0)
            json.dump(loaded_data, f, indent=2)

            f.close()

            return {"message": "Successfully . .", "status": True}
        else:
            return {"message": "Failed . . .", "status": False}


def delete(file, table, data):
    try:
        with open(file, 'r') as f:
            loaded_data = json.load(f)

    except FileNotFoundError as e:
        print(e)
        return False

    except json.decoder.JSONDecodeError as e:
        print(e)
        return False

    except Exception as e:
        print(e)
        return False

    else:
        if table in loaded_data:

            for i in loaded_data[table]:
                if i[data['uniqueKey']] == data['uniqueValue']:
                    loaded_data[table].remove(i)

            with open(file, 'w') as f:
                json.dump(loaded_data, f, indent=2)

            f.close()

            return {"message": "Successfully deleted . . .", "status": True}
        else:
            return {"message": "Table not found . . .", "status": False}
