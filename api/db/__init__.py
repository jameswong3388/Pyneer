import json

database = 'database/db.json'


def insert_one(collection, document, file=database):
    """
    This function create single record in the collection
    (:param) file: File used to store the data
    (:param) collection: Collection to be used to store the data
    (:param) document: Data in the form of a dictionary

    e.g. document = {'username': 'admin', ...}

    if the collection does not exist, it will be created
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    else:

        if isinstance(document, dict) and document != {}:
            if collection in loaded_data:
                loaded_data[collection].append(document)

                f.seek(0)
                json.dump(loaded_data, f, indent=2)

                f.close()

                return {"message": "Successful.", "action": True}

            else:
                create_collection(collection=collection, file=file)

                insert_one(collection=collection, document=document, file=file)

                return {"message": "Successful.", "action": True}

        else:
            return {"message": "Failed.", "action": False}


def insert_many(collection, documents, file=database):
    """
    This function create single record in the collection
    (:param) file: File used to store the data
    (:param) collection: Collection to be used to store the data
    (:param) documents: Data in the form of a dictionary

    e.g. documents = [{'username': 'admin', ...}, {'username': 'admin', ...}]

    if the collection does not exist, it will be created
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    else:

        if isinstance(documents, list) and documents != []:
            if collection in loaded_data:
                for i in documents:
                    if i != {}:
                        loaded_data[collection].append(i)

                    else:
                        return {"message": "Failed.", "action": False}

                f.seek(0)
                json.dump(loaded_data, f, indent=2)

                f.close()

                return {"message": "Successful.", "action": True}

            else:
                create_collection(collection=collection, file=file)

                insert_many(collection=collection, documents=documents, file=file)

                return {"message": "Successful.", "action": True}

        else:
            return {"message": "Failed.", "action": False}


def read(collection, query, file=database):
    """
    This function reads a record from the collection

    (:param) file: File used to store the data
    (:param) collection: Collection to be used to store the data
    (:param) query: An array of keys to be queried from the collection

    e.g. query = ['username', 'password', 'role']
    if query = [] then all the documents in the collection will be returned
   """

    new_lists = []

    try:
        f = open(file, 'r')
        loaded_data = json.loads(f.read())

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    else:
        if isinstance(query, list) and collection in loaded_data:
            if query:

                for i in loaded_data[collection]:
                    new_dict = {}

                    for key in query:

                        if key in i and key != '':

                            new_dict[key] = i[key]

                        else:
                            return {"message": "Invalid Key.", "action": False}

                    new_lists.append(new_dict)

                f.close()

                return {"message": "Successful.", "action": True, "result": new_lists}

            else:
                return {"message": "Successful.", "action": True, "result": loaded_data[collection]}

        else:
            return {"message": "Failed.", "action": False, "result": []}


def find(query, collection, file=database):
    """
    This function will query from 'file' and return a result
    with all the data that matches the key and value.

    (:param) query: The query to be used to search the database
    (:param) collection: Collection's name

    e.g. query = {"key": "...", "value": "..."}
    if nothing is found, it will return an empty list, []
    if query = {} then all the documents in the collection will be returned
    """

    read_data = read(collection=collection, query=[], file=file)

    if read_data['action'] and read_data['result'] and query != {}:
        new_result = []

        for data in read_data['result']:
            try:
                if data[query['key']] == query['value']:
                    new_dict = data
                    new_result.append(new_dict)

            except KeyError:
                return {'action': False, 'message': 'Invalid Key.'}

        return {'action': True, 'message': "Successful.", 'result': new_result}

    elif read_data['action'] and read_data['result'] and query == {}:
        return {'action': True, 'message': "Successful.", 'result': read_data['result']}

    else:
        return {'action': False, 'message': 'No data found'}


def update_one(collection, data, file=database):
    """
    This function update a single record in the collection

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
        f.close()

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    else:
        flag = False

        if isinstance(data, dict) and data != {} and collection in loaded_data and data['unique_key'] != '' and \
                data['unique_value'] != '':
            for i in loaded_data[collection]:
                if data['key'] != '' and data['value'] and i[data['unique_key']] == data['unique_value'] \
                        and data['key'] in i:

                    try:
                        i[data['key']] = data['value']

                    except KeyError:
                        return {"message": "Invalid Key.", "action": False}

                    else:

                        with open(file, 'w+') as f:
                            f.seek(0)
                            json.dump(loaded_data, f, indent=2)
                        f.close()

                        return {"message": "Successful.", "action": True}

            if not flag:
                return {"message": "Failed.", "action": False}

        else:
            return {"message": "Failed.", "action": False}


def update_many(collection, data, file=database):
    """
    This function updates multiple records in the collection

    (:param) file: The file used to store the data
    (:param) collection: The collection to be used to store the data
    (:param) data: Data in the form of a list of dictionaries

    e.g. data = [{'unique_key': 'username', 'unique_value': 'admin', 'key': 'role', 'value': 'admin'}, ...]
    where unique_key and unique_value  is the key value used to identify the record to be updated,
    and key and value is the key value to be updated.
    """

    try:
        f = open(file, 'r+')
        loaded_data = json.load(f)
        f.close()

    except FileNotFoundError as e:
        return {"message": str(e), "action": False}

    except json.decoder.JSONDecodeError as e:
        return {"message": str(e), "action": False}

    else:
        flag = False

        if isinstance(data, list) and data != [] and collection in loaded_data:
            for i in data:
                if i['unique_key'] != '' and i['unique_value'] != '' and i['key'] != '' and i['value'] != '':
                    for j in loaded_data[collection]:
                        try:
                            if j[i['unique_key']] == i['unique_value'] and i['key'] in j:

                                try:
                                    j[i['key']] = i['value']

                                except KeyError:
                                    return {"message": "Invalid Key.", "action": False}

                                else:
                                    with open(file, 'w+') as f:
                                        f.seek(0)
                                        json.dump(loaded_data, f, indent=2)

                                    flag = True

                            else:
                                flag = False

                        except KeyError:
                            return {"message": "Invalid Key.", "action": False}

            f.close()

            if flag:
                return {"message": "Successful.", "action": True}

            else:
                return {"message": "Failed.", "action": False}

        else:
            return {"message": "Failed.", "action": False}


def delete_one(collection, data, file=database):
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

                                return {"message": "Successful.", "action": True}

                    except KeyError:
                        return {"message": "Invalid Key.", "action": False}

                if not flag:
                    return {"message": "Failed.", "action": False}

        else:
            return {"message": "Failed.", "action": False}


def delete_many(collection, data, file=database):
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

    else:
        flag = False

        if isinstance(data, list) and data != [] and collection in loaded_data:

            for i in data:
                if i['unique_key'] != '' and i['unique_value'] != '':

                    for j in loaded_data[collection]:
                        try:
                            if j[i['unique_key']] == i['unique_value'] and i['unique_key'] in j:
                                try:
                                    loaded_data[collection].remove(j)

                                except ValueError as e:
                                    return {"message": str(e), "action": False}

                                else:
                                    f = open(file, 'w')
                                    json.dump(loaded_data, f, indent=2)
                                    f.close()

                                    flag = True

                        except KeyError:
                            return {"message": "Invalid Key.", "action": False}

                else:
                    return {"message": "Failed.", "action": False}

            if flag:
                return {"message": "Successful.", "action": True}

            else:
                return {"message": "Failed.", "action": False}

        else:
            return {"message": "Failed.", "action": False}


def create_db(file):
    """
    This function creates a database
    (:param) file: The file used to store the data
    """

    try:
        f = open(file, 'x')
        json.dump({}, f, indent=2)
        f.close()

    except FileExistsError as e:
        return {"message": str(e), "action": False}

    else:
        return {"message": "Successfully.", "action": True}


def create_collection(collection, file=database):
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

    else:
        try:
            if collection not in loaded_data and collection != '':
                loaded_data[collection] = []

            else:
                return {"message": "Collection already exists or Invalid collection name", "action": False}

        except KeyError as e:
            return {"message": str(e), "action": False}

        else:
            f.seek(0)
            json.dump(loaded_data, f, indent=2)
            f.close()

            return {"message": "Successfully.", "action": True}


def drop_collection(collection, file=database):
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

    else:

        try:
            if collection in loaded_data and collection != '':

                loaded_data.pop(collection)

            else:
                return {"message": "Collection does not exist or Invalid collection name", "action": False}

        except KeyError as e:
            return {"message": str(e), "action": False}

        else:
            with open(file, 'w') as f:

                json.dump(loaded_data, f, indent=2)

                f.close()

            return {"message": "Successfully.", "action": True}


def count(collection, query, file=database):
    """
    This function counts the number of records in a collection

    (:param) collection: The collection to be used to store the data

    if query = {} then it counts all the documents in the collection
    """

    read_data = find(query=query, collection=collection, file=file)

    if read_data['action']:
        return {"message": "Successfully.", "action": True, "count": len(read_data['result'])}

    else:
        return {"message": "Collection does not exist or Invalid collection name", "action": False}


def generate_new_id(collection, file=database):
    """
    This function will get the last id of the collection and add 1 to it.

    (:param) collection: The collection name
    """
    read_data = read(collection=collection, query=['id'], file=file)

    if read_data['action'] and read_data['result']:
        new_id = int(read_data['result'][-1]["id"]) + 1
        return {'action': True, 'message': "", 'result': new_id}

    else:
        return {'action': False, 'message': 'No data found.'}


def db():
    """
    This function will return all the database in 'database' folder
    """
    import os

    files = os.listdir('database')

    return files


def total_size(collection, file=database):
    """
    This function will return the total size of the collection

    (:param) file: The file used to store the data

    return the size in bytes
    """

    import sys

    loaded_data = read(collection=collection, file=file, query=[])

    if loaded_data['action']:
        return {'action': True, 'message': '', 'result': str(sys.getsizeof(loaded_data['result'])) + ' bytes'}

    else:
        return {'action': False, 'message': 'No data found.'}
