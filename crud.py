import json


def create(file, table, data):
    """
    This function creates a new record in the table
    (:param) file: File used to store the data
    (:param) table: Table to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = {'username': 'admin', 'password': 'admin', 'role': 'admin'}

    if the table does not exist, it will be created
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": e, "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": e, "status": False}

    except Exception as e:
        return {"message": e, "status": False}

    else:

        if isinstance(data, dict) and data != {}:
            if table in loaded_data:
                loaded_data[table].append(data)

                f.seek(0)
                json.dump(loaded_data, f, indent=2)

                f.close()

                return {"message": "Successful . . .", "status": True}

            else:
                create_table(table)

                create(file, table, data)

                return {"message": "Successful . . .", "status": True}

        else:
            return {"message": "Failed . . .", "status": False}


def read(file, table, queried_key):
    """
    This function reads a record from the table

    (:param) file: File used to store the data
    (:param) table: Table to be used to store the data
    (:param) queried_key: An array of keys to be queried from the table

    e.g. queried_key = ['username', 'password', 'role']
    if queried_key = [] then all the keys in the table will be queried
    """

    new_lists = []

    try:
        f = open(file, 'r')
        loaded_data = json.loads(f.read())

    except FileNotFoundError as e:
        return {"message": str(e), "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "status": False}

    except Exception as e:
        return {"message": str(e), "status": False}

    else:
        if isinstance(queried_key, list) and table in loaded_data:
            if queried_key:

                for i in loaded_data[table]:
                    new_dict = {}

                    for key in queried_key:

                        if key in i and key != '':

                            new_dict[key] = i[key]

                        else:
                            return {"message": "Invalid Key . . .", "status": False}

                    new_lists.append(new_dict)

                f.close()

                return {"message": "Successfully . . . ", "status": True, "result": new_lists}
            else:
                return {"message": "Successfully . . . ", "status": True, "result": loaded_data[table]}

        else:
            return {"message": "Failed . . .", "status": False, "result": []}


def update(file, table, data):
    """
    This function updates a record in the table

    (:param) file: The file used to store the data
    (:param) table: The table to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = {'unique_key': 'username', 'unique_value': 'admin', 'key': 'role', 'value': 'admin'}
    where unique_key and unique_value  is the key value used to identify the record to be updated,
    and key and value is the key value to be updated.
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": str(e), "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "status": False}

    except Exception as e:
        return {"message": str(e), "status": False}

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
    """
    This function deletes a record from the table

    (:param) file: The file used to store the data
    (:param) table: The table to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = {'unique_key': 'username', 'unique_value': 'admin'}
    where unique_key and unique_value  is the key value used to identify the record to be deleted.

    if data = {} then all the records in the table will be deleted.
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)
        f.close()

    except FileNotFoundError as e:
        return {"message": str(e), "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "status": False}

    except Exception as e:
        return {"message": str(e), "status": False}

    else:
        flag = False

        if isinstance(data, dict) and table in loaded_data:

            if data != {} and data['unique_key'] != '' and data['unique_value'] != '':

                for i in loaded_data[table]:
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

            else:
                loaded_data[table] = []

                with open(file, 'w') as f:
                    json.dump(loaded_data, f, indent=2)

                f.close()

                return {"message": "Successfully . . .", "status": True}

        else:
            return {"message": "Failed . . .", "status": False}


def create_table(table):
    """
    This function creates a table

    (:param) table: The table to be created
    """

    try:
        f = open('database.json', 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": str(e), "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "status": False}

    except Exception as e:
        return {"message": str(e), "status": False}

    else:

        try:
            if table not in loaded_data and table != '':
                loaded_data[table] = []

            else:
                raise Exception("Table already exists or Invalid table name")

        except KeyError as e:
            return {"message": str(e), "status": False}

        except Exception as e:
            return {"message": str(e), "status": False}

        else:
            f.seek(0)
            json.dump(loaded_data, f, indent=2)
            f.close()

            return {"message": "Successfully . . .", "status": True}


def delete_table(table):
    """
    This function deletes a table

    (:param) table: The table to be deleted
    """

    try:
        f = open('database.json', 'r+')
        loaded_data = json.load(f)
        f.close()

    except FileNotFoundError as e:
        return {"message": str(e), "status": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "status": False}

    except Exception as e:
        return {"message": str(e), "status": False}

    else:

        try:
            if table in loaded_data and table != '':

                loaded_data.pop(table)

            else:
                raise Exception("Table does not exist or Invalid table name")

        except KeyError as e:
            return {"message": str(e), "status": False}

        except Exception as e:
            return {"message": str(e), "status": False}

        else:
            with open('database.json', 'w') as f:

                json.dump(loaded_data, f, indent=2)

                f.close()

            return {"message": "Successfully . . .", "status": True}
