import json


def create(file, mode, table, data):
    # data is a dictionary with the following keys and values:
    # e.g. {'username': 'admin', 'password': 'admin', 'role': 'admin'}

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
        if isinstance(data, dict) and data != {} and table in loaded_data:
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
        if isinstance(queried_key, list) and queried_key != [] and table in loaded_data:

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

        flag = False

        if isinstance(data, dict) and data != {} and table in loaded_data and data['unique_key'] != '' and \
                data['unique_value'] != '':
            for i in loaded_data[table]:
                if data['key'] != '' and data['value'] != '' and i[data['unique_key']] == data['unique_value'] \
                        and data['key'] in i:

                    try:
                        i[data['key']] = data['value']

                    except KeyError as e:
                        return {"message": e, "status": False}

                    else:
                        f.seek(0)
                        json.dump(loaded_data, f, indent=2)

                        f.close()

                        return {"message": "Successful . . .", "status": True}

            if not flag:
                return {"message": "Failed . . .", "status": False}

        else:
            return {"message": "Failed . . .", "status": False}


def delete(file, table, data):
    # data is a dictionary with the following keys:
    # unique_key, unique_value

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)
        f.close()

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

        flag = False

        if isinstance(data, dict) and table in loaded_data and data != {} and data['unique_key'] != '' and \
                data['unique_value'] != '':

            print(loaded_data[table])

            for i in loaded_data[table]:

                # i['id'] == 7
                print(i[data['unique_key']])
                print(data['unique_value'])

                print(i[data['unique_key']] == data['unique_value'])

                # unique_key = id and unique_value = 7

                if i[data['unique_key']] == data['unique_value'] and data['unique_key'] in i:

                    try:
                        loaded_data[table].remove(i)

                    except ValueError as e:
                        return {"message": e, "status": False}

                    else:
                        f = open(file, 'w')
                        json.dump(loaded_data, f, indent=2)
                        f.close()

                        return {"message": "Successful . . .", "status": True}

            if not flag:
                return {"message": "Failed . . .", "status": False}

        elif isinstance(data, dict) and data == {} and table in loaded_data:

            loaded_data[table] = []

            with open(file, 'w') as f:
                json.dump(loaded_data, f, indent=2)

            f.close()

            return {"message": "Successfully . . .", "status": True}

        else:
            return {"message": "Failed . . .", "status": False}
