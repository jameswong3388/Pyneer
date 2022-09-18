import json


def insert_one(collection, data, file='database/db.json'):
    """
    This function create single record in the collection
    (:param) file: File used to store the data
    (:param) collection: Collection to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = {'username': 'admin', ...}

    if the collection does not exist, it will be created
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": e, "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": e, "action": False}

    except Exception as e:
        return {"message": e, "action": False}

    else:

        if isinstance(data, dict) and data != {}:
            if collection in loaded_data:
                loaded_data[collection].append(data)

                f.seek(0)
                json.dump(loaded_data, f, indent=2)

                f.close()

                return {"message": "Successful . . .", "action": True}

            else:
                create_collection(collection=collection, file=file)

                insert_one(collection=collection, data=data, file=file)

                return {"message": "Successful . . .", "action": True}

        else:
            return {"message": "Failed . . .", "action": False}


def insert_many(collection, data, file='database/db.json'):
    """
    This function create single record in the collection
    (:param) file: File used to store the data
    (:param) collection: Collection to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = [{'username': 'admin', ...}, {'username': 'admin', ...}]

    if the collection does not exist, it will be created
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": e, "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": e, "action": False}

    except Exception as e:
        return {"message": e, "action": False}

    else:

        if isinstance(data, list) and data != []:
            if collection in loaded_data:
                for i in data:
                    if i != {}:
                        loaded_data[collection].append(i)

                    else:
                        return {"message": "Failed . . .", "action": False}

                f.seek(0)
                json.dump(loaded_data, f, indent=2)

                f.close()

                return {"message": "Successful . . .", "action": True}

            else:
                create_collection(collection=collection, file=file)

                insert_many(collection=collection, data=data, file=file)

                return {"message": "Successful . . .", "action": True}

        else:
            return {"message": "Failed . . .", "action": False}


def read(collection, queried_key, file='database/db.json'):
    """
    This function reads a record from the collection

    (:param) file: File used to store the data
    (:param) collection: Collection to be used to store the data
    (:param) queried_key: An array of keys to be queried from the collection

    e.g. queried_key = ['username', 'password', 'role']
    if queried_key = [] then all the keys in the collection will be queried
    """

    new_lists = []

    try:
        f = open(file, 'r')
        loaded_data = json.loads(f.read())

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    except Exception as e:
        return {"message": str(e), "action": False}

    else:
        if isinstance(queried_key, list) and collection in loaded_data:
            if queried_key:

                for i in loaded_data[collection]:
                    new_dict = {}

                    for key in queried_key:

                        if key in i and key != '':

                            new_dict[key] = i[key]

                        else:
                            return {"message": "Invalid Key . . .", "action": False}

                    new_lists.append(new_dict)

                f.close()

                return {"message": "Successfully . . . ", "action": True, "result": new_lists}
            else:
                return {"message": "Successfully . . . ", "action": True, "result": loaded_data[collection]}

        else:
            return {"message": "Failed . . .", "action": False, "result": []}


def find(key, value, collection, file='database/db.json'):
    """
    This function will query from 'file' and return a result
    with all the data that matches the key and value.

    (:param) key: Dictionary key
    (:param) value: Dictionary value
    (:param) collection: Collection's name

    if nothing is found, it will return an empty list, []
    """

    read_data = read(collection=collection, queried_key=[], file=file)

    if read_data['action'] and read_data['result']:

        new_result = []

        for data in read_data['result']:
            try:
                if data[key] == value:
                    new_dict = data
                    new_result.append(new_dict)

            except KeyError:
                return {'action': False, 'message': 'Key not found.'}

        return {'action': True, 'message': "", 'result': new_result}

    else:
        return {'action': False, 'message': 'No data found'}


def update_one(collection, data, file='database/db.json'):
    """
    This function update single record in the collection

    (:param) file: The file used to store the data
    (:param) collection: The collection to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = {'unique_key': 'username', 'unique_value': 'admin', 'key': 'role', 'value': 'admin'}
    where unique_key and unique_value  is the key value used to identify the record to be updated,
    and key and value is the key value to be updated.
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    except Exception as e:
        return {"message": str(e), "action": False}

    else:

        flag = False

        if isinstance(data, dict) and data != {} and collection in loaded_data and data['unique_key'] != '' and \
                data['unique_value'] != '':
            for i in loaded_data[collection]:
                if data['key'] != '' and data['value'] != '' and i[data['unique_key']] == data['unique_value'] \
                        and data['key'] in i:

                    try:
                        i[data['key']] = data['value']

                    except KeyError:
                        return {"message": "Key not found", "action": False}

                    else:
                        f.seek(0)
                        json.dump(loaded_data, f, indent=2)

                        f.close()

                        return {"message": "Successful . . .", "action": True}

            if not flag:
                return {"message": "Failed . . .", "action": False}

        else:
            return {"message": "Failed . . .", "action": False}


def delete_one(collection, data, file='database/db.json'):
    """
    This function deletes a record from the collection

    (:param) file: The file used to store the data
    (:param) collection: The collection to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = {'unique_key': 'username', 'unique_value': 'admin'}
    where unique_key and unique_value  is the key value used to identify the record to be deleted.
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)
        f.close()

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    except Exception as e:
        return {"message": str(e), "action": False}

    else:
        flag = False

        if isinstance(data, dict) and collection in loaded_data:

            if data != {} and data['unique_key'] != '' and data['unique_value'] != '':

                for i in loaded_data[collection]:
                    try:
                        if i[data['unique_key']] == data['unique_value'] and data['unique_key'] in i:

                            try:
                                loaded_data[collection].remove(i)

                            except ValueError as e:
                                return {"message": e, "action": False}

                            else:
                                f = open(file, 'w')
                                json.dump(loaded_data, f, indent=2)
                                f.close()

                                return {"message": "Successful . . .", "action": True}

                    except KeyError:
                        return {"message": "Key not found", "action": False}

                if not flag:
                    return {"message": "Failed . . .", "action": False}

        else:
            return {"message": "Failed . . .", "action": False}


def delete_many(collection, data, file='database/db.json'):
    """
    This function delete multiple records from the collection

    (:param) file: The file used to store the data
    (:param) collection: The collection to be used to store the data
    (:param) data: Data in the form of a dictionary

    e.g. data = [{'unique_key': 'username', 'unique_value': 'admin'}, ...]
    where key and value is the key value used to identify the records to be deleted.
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)
        f.close()

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    except Exception as e:
        return {"message": str(e), "action": False}

    else:

        if isinstance(data, list) and data != [] and collection in loaded_data:

            for i in data:
                if i['unique_key'] != '' and i['unique_value'] != '':
                    flag = False

                    for j in loaded_data[collection]:
                        try:
                            if j[i['unique_key']] == i['unique_value'] and i['unique_key'] in j:
                                try:
                                    loaded_data[collection].remove(j)

                                except ValueError as e:
                                    return {"message": e, "action": False}

                                else:
                                    f = open(file, 'w')
                                    json.dump(loaded_data, f, indent=2)
                                    f.close()

                                    flag = True

                        except KeyError:
                            return {"message": "Key not found", "action": False}

                    if not flag:
                        return {"message": "Failed . . .", "action": False}

                else:
                    return {"message": "Failed . . .", "action": False}

            return {"message": "Successful . . .", "action": True}

        else:
            return {"message": "Failed . . .", "action": False}


def create_collection(collection, file='database/db.json'):
    """
    This function creates a collection

    (:param) collection: The collection to be created
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    except Exception as e:
        return {"message": str(e), "action": False}

    else:

        try:
            if collection not in loaded_data and collection != '':
                loaded_data[collection] = []

            else:
                raise Exception("Collection already exists or Invalid collection name")

        except KeyError as e:
            return {"message": str(e), "action": False}

        except Exception as e:
            return {"message": str(e), "action": False}

        else:
            f.seek(0)
            json.dump(loaded_data, f, indent=2)
            f.close()

            return {"message": "Successfully . . .", "action": True}


def drop_collection(collection, file='database/db.json'):
    """
    This function deletes a collection

    (:param) collection: The collection to be deleted
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)
        f.close()

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    except Exception as e:
        return {"message": str(e), "action": False}

    else:

        try:
            if collection in loaded_data and collection != '':

                loaded_data.pop(collection)

            else:
                raise Exception("Collection does not exist or Invalid collection name")

        except KeyError as e:
            return {"message": str(e), "action": False}

        except Exception as e:
            return {"message": str(e), "action": False}

        else:
            with open(file, 'w') as f:

                json.dump(loaded_data, f, indent=2)

                f.close()

            return {"message": "Successfully . . .", "action": True}


def generate_new_id(collection, file='database/db.json'):
    """
    This function will get the last id of the collection and add 1 to it.

    (:param) collection: The collection name
    """

    read_data = read(collection=collection, queried_key=['id'], file=file)

    if read_data['action'] and read_data['result']:
        new_id = read_data['result'][-1]['id'] + 1
        return {'action': True, 'message': "", 'result': new_id}

    else:
        return {'action': False, 'message': 'No data found'}


def db():
    """
    This function will return all the database in 'database' folder
    """
    import os

    files = os.listdir('database')

    return files
