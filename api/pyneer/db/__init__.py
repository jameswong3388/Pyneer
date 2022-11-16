"""
Pyneer's `db.*` API
"""
import json
import os
import uuid

from api.pyneer.db import handlers

DEFAULT_DATABASE_PATH = 'database/db.json'


def insert_one(collection, document, db_path=DEFAULT_DATABASE_PATH):
    """ This function create single record in the collection

    :param collection: Collection to be used to store the data
    :param document: Data in the form of a dictionary
    :param db_path: File used to store the data

    e.g. document = {'key': 'value', ...}

    Note: If the collection does not exist, it will be created.
    Note: '_id' will be generated if it does not exist.
    """

    if not isinstance(document, dict):
        return {"action": False, "message": "Document is not a dictionary"}

    if not document:
        return {"action": False, "message": "Document is empty"}

    with handlers.file_handler(mode='r+', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

        if collection in loaded_data:
            if '_id' not in document.keys():
                _id = generate__id(collection=collection, db_path=db_path)['_id']
                document['_id'] = _id

            if document['_id'] in [i['_id'] for i in loaded_data[collection]]:
                return {"action": False, "message": "Duplicate key error for _id"}

            loaded_data[collection].append(document)
            inserted_id = document['_id'] or _id

            f['file'].seek(0)
            json.dump(loaded_data, f['file'], indent=2)

            return {"action": True, "inserted_id": inserted_id}

        else:
            create_collection(collection=collection, db_path=db_path)
            r = insert_one(collection=collection, document=document, db_path=db_path)

            return {"action": True, "inserted_id": r['inserted_id']}


def insert_many(collection, documents, db_path=DEFAULT_DATABASE_PATH):
    """This function create single record in the collection

    :param collection: Collection to be used to store the data
    :param documents: Data in the form of a dictionary
    :param db_path: File used to store the data

    e.g. documents = [{'key': 'value', ...}, {'key': 'value', ...}]

    Note: If the collection does not exist, it will be created.
    Note: If the document = {} then it will skip.
    Note: '_id' will be generated if it does not exist, if duplicate '_id' is found, the remaining documents will be
    skipped.
    """

    if not isinstance(documents, list):
        return {"action": False, "message": "Documents is not a list"}

    if not documents:
        return {"action": False, "message": "Documents is empty"}

    with handlers.file_handler(mode='r+', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

    if collection in loaded_data:
        _ids = []

        for i in documents:
            if i != {}:
                if '_id' not in i.keys():
                    _id = generate__id(collection=collection, db_path=db_path)['_id']
                    i['_id'] = _id
                    _ids.append(_id)
                else:
                    if i['_id'] in [i['_id'] for i in loaded_data[collection]]:
                        return {"action": False, "message": "Duplicate key error for _id", "inserted_ids": _ids}

                    _ids.append(i['_id'])

                loaded_data[collection].append(i)

                with open(db_path, 'w') as f:
                    f.seek(0)
                    json.dump(loaded_data, f, indent=2)

            else:
                continue

        return {"action": True, "inserted_ids": _ids}

    else:
        create_collection(collection=collection, db_path=db_path)
        r = insert_many(collection=collection, documents=documents, db_path=db_path)

        return {"action": True, "inserted_ids": r["inserted_ids"]}


def read(collection, query=[], db_path=DEFAULT_DATABASE_PATH):
    """This function reads a record from the collection

    :param collection: Collection to be used to store the data
    :param query: An array of keys to be queried from the collection
    :param db_path: File used to read the data

    e.g. query = ['username', 'password', 'role']

    Note: If query = [] then all the documents in the collection will be returned.
    Note: If key does not exist, it will be skipped.
   """

    if not isinstance(query, list):
        return {"action": False, "message": "Query is not a list"}

    with handlers.file_handler(mode='r', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

        try:
            if query:
                new_lists = []

                for i in loaded_data[collection]:
                    new_dict = {}

                    for key in query:
                        if key in i:
                            new_dict[key] = i[key]
                            new_lists.append(new_dict)

                        else:
                            continue

                return {"action": True, "matched_count": len(new_lists),
                        "result": new_lists}

            return {"action": True, "matched_count": len(loaded_data[collection]),
                    "result": loaded_data[collection]}

        except KeyError:
            return {"action": False, "message": "Collection does not exist"}


def find(collection, query={}, db_path=DEFAULT_DATABASE_PATH):
    """This function will query from 'file' and return a result
    with all the data that matches the key and value.

    :param collection: Collection's name
    :param query: The query to be used to search the database
    :param db_path: The file used to find the data

    e.g. query = {'key': 'value', ...}
    Note: If nothing is found, it will return an empty list, [].
    Note: If query = {} then all the documents in the collection will be returned.
    """

    read_data = read(collection=collection, db_path=db_path)

    if not isinstance(query, dict):
        return {"action": False, "message": "Query is not a dictionary"}

    if read_data['action'] and read_data['result']:
        r = filtr(data=read_data['result'], query=query)

        return {"action": True, 'matched_count': r['matched_count'], "result": r['result']}

    else:
        return {'action': False, 'message': read_data['message']}


def filtr(data, query):
    """This function will filter the data based on the field

    :param data: The data to be filtered
    :param query: The field to be used to filter the data

    e.g. field = {'key': 'value', ...}
    e.g. data = [{'key': 'value', ...}, {'key2': 'value2', ...}]

    Note: If query = {} then all the documents in the collection will be returned.
    Note: This function does not supoort nested filtration yet,
    e.g. filtr(data={'a': {{'a': [1,2,3], 'b': {}}}}, query={'b': 1})
    """

    result = list(filter(lambda x: all(item in x.items() for item in query.items()), data))
    matched_count = len(result)

    return {'acknowledge': True if matched_count > 0 else False, 'matched_count': matched_count, 'result': result}


def update_one(collection, select, update, db_path=DEFAULT_DATABASE_PATH):
    """This function update a single record in the collection

    :param collection: The collection to be used to store the data
    :param select: select: The filter to be used to identify the record to be updated
    :param update: The data to be used to update the record
    :param db_path: The file used to update the data

    e.g. select = {'key': 'value', ...}
    e.g. update = {'key': 'value', ...}

    Note: If the Key in the select does not exist, it will be created and the value will be updated.
    Note: This method will only update the first record that matches the select.
    """

    if not isinstance(select, dict):
        return {"action": False, 'message': 'Select is not a dictionary'}

    if not isinstance(update, dict):
        return {"action": False, 'message': 'Update is not a dictionary'}

    if update == {}:
        return {"action": False, 'message': 'Update is empty'}

    with handlers.file_handler(mode='r', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

    try:
        a = filtr(data=loaded_data[collection], query=select)

        if a['acknowledge']:
            for i in a['result']:
                for key, value in update.items():
                    i[key] = value

                break

            with open(db_path, 'w+') as f:
                f.seek(0)
                json.dump(loaded_data, f, indent=2)

            return {"action": True, "modified_count": 1, "matched_count": a['matched_count']}

        else:
            return {"action": False, "modified_count": 0, "matched_count": a['matched_count']}

    except KeyError:
        return {"action": False, 'message': 'Collection does not exist'}


def update_many(collection, select, update, db_path=DEFAULT_DATABASE_PATH):
    """
    This function updates multiple records in the collection

    :param collection: The collection to be used to store the data
    :param select: select: The filter to be used to identify the records to be updated
    :param update: The data to be used to update the records
    :param db_path: The file used to update the data

    e.g. select = {'key': 'value', ...}
    e.g. update = {'key': 'value', ...}
    """

    if not isinstance(select, dict):
        return {"action": False, 'message': 'Select is not a dictionary'}

    if not isinstance(update, dict):
        return {"action": False, 'message': 'Update is not a dictionary'}

    if update == {}:
        return {"action": False, 'message': 'Update is empty'}

    with handlers.file_handler(mode='r', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

    try:
        modified_count = 0
        a = filtr(data=loaded_data[collection], query=select)

        if a['acknowledge']:
            for i in a['result']:
                for key, value in update.items():
                    i[key] = value

                modified_count += 1

            with open(db_path, 'w+') as f:
                f.seek(0)
                json.dump(loaded_data, f, indent=2)

            return {"action": True, "modified_count": modified_count, "matched_count": a['matched_count']}

        else:
            return {"action": False, "modified_count": modified_count, "matched_count": a['matched_count']}

    except KeyError:
        return {"action": False, 'message': 'Collection does not exist'}


def replace_one(collection, select, replacement, db_path=DEFAULT_DATABASE_PATH):
    """This function replace a single record in the collection

    :param collection: The collection to be used to store the data
    :param select: The filter to be used to identify the record to be replaced
    :param replacement: The replacement to be used to replace the record
    :param db_path: The file used to store the data

    e.g. select = {'key': 'value', ...}
    e.g. replacement = {'key': 'value', ...}
    Note: This method will only update the first record that matches the select.
    Note: '_id' will be generated if it does not exist.
    """

    if not isinstance(select, dict):
        return {"action": False, 'message': 'Select is not a dictionary'}

    if not isinstance(replacement, dict):
        return {"action": False, 'message': 'Replacement is not a dictionary'}

    if replacement == {}:
        return {"action": False, 'message': 'Replacement is empty'}

    with handlers.file_handler(mode='r', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

    try:
        a = filtr(data=loaded_data[collection], query=select)

        if a['acknowledge']:
            for i in a['result']:

                if '_id' not in replacement:
                    _id = generate__id(collection=collection, db_path=db_path)['_id']
                    replacement['_id'] = _id

                if replacement['_id'] in [i['_id'] for i in loaded_data[collection]]:
                    return {"action": False, "message": "Duplicate key error for _id"}

                i.clear()
                i.update(replacement)
                break

            with open(db_path, 'w+') as f:
                f.seek(0)
                json.dump(loaded_data, f, indent=2)

            return {"action": True, "modified_count": 1, "matched_count": a['matched_count']}
        else:
            return {"action": False, "modified_count": 0, "matched_count": a['matched_count']}

    except KeyError:
        return {"action": False, 'message': 'Collection does not exist'}


def delete_one(collection, select, db_path=DEFAULT_DATABASE_PATH):
    """This function deletes a record from the collection

    :param collection: The collection to be used to store the data
    :param select: The filter to be used to identify the record to be deleted
    :param db_path: The file used to store the data

    e.g. select = {'key': 'value', ...}
    """

    if not isinstance(select, dict):
        return {"action": False, 'message': 'Select is not a dictionary'}

    if select == {}:
        return {"action": False, 'message': 'Select is empty'}

    with handlers.file_handler(mode='r', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

    try:
        a = filtr(data=loaded_data[collection], query=select)

        if a['acknowledge']:
            for i in a['result']:
                loaded_data[collection].remove(i)
                break

            with open(db_path, 'w+') as f:
                f.seek(0)
                json.dump(loaded_data, f, indent=2)

            return {"action": True, "deleted_count": 1, "matched_count": a['matched_count']}
        else:
            return {"action": False, "deleted_count": 0, "matched_count": a['matched_count']}

    except KeyError:
        return {"action": False, 'message': 'Collection does not exist'}


def delete_many(collection, select, db_path=DEFAULT_DATABASE_PATH):
    """
    This function delete multiple records from the collection

    :param collection: The collection to be used to store the data
    :param select: The filters to be used to identify the records to be deleted
    :param db_path: The file used to store the data

    e.g. select = {'key': 'value', ...}
    where key and value is the key value used to identify the records to be deleted.
    """

    if not isinstance(select, dict):
        return {"action": False, 'message': 'Select is not a dictionary'}

    if select == {}:
        return {"action": False, 'message': 'Select is empty'}

    with handlers.file_handler(mode='r', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

    try:
        a = filtr(data=loaded_data[collection], query=select)

        if a['acknowledge']:
            for i in a['result']:
                loaded_data[collection].remove(i)

            with open(db_path, 'w+') as f:
                f.seek(0)
                json.dump(loaded_data, f, indent=2)

            return {"action": True, "deleted_count": a['matched_count'], "matched_count": a['matched_count']}
        else:
            return {"action": False, "deleted_count": 0, "matched_count": a['matched_count']}

    except KeyError:
        return {"action": False, 'message': 'Collection does not exist'}


def create_db(file_path):
    """This function creates a database file

    :param file_path: The file used to store the data

    e.g. file_path = 'path/to/file.json'
    """

    try:
        with open(file_path, mode='x', encoding='utf-8') as f:
            json.dump({}, f, indent=2)

        return {"action": True}

    except FileExistsError:
        return {"action": False, "message": "File already exist"}


def create_collection(collection, db_path=DEFAULT_DATABASE_PATH):
    """This function creates a collection

    :param collection: The collection to be created
    :param db_path: The file used to store the data

    e.g. collection = 'collection_name'
    """

    if collection == '':
        return {"action": False, "message": "Collection name cannot be empty"}

    with handlers.file_handler(mode='r+', file_path=db_path) as f:
        if not f['action']:
            return {"action": False, "message": "File does not exist"}

        loaded_data = f["loaded_data"]

        if collection not in loaded_data:
            loaded_data[collection] = []

            f['file'].seek(0)
            json.dump(loaded_data, f['file'], indent=2)

            return {"action": True}

        else:
            return {"action": False, "message": "Collection already exist"}


def drop_db(db_path=DEFAULT_DATABASE_PATH):
    """This function deletes a database file

    :param db_path: The file used to store the data
    """

    try:
        os.remove(db_path)

        return {"action": True}

    except FileNotFoundError:
        return {"action": False, "message": "File does not exist"}


def drop_collection(collection, db_path=DEFAULT_DATABASE_PATH):
    """This function deletes a collection

    :param collection: The collection to be deleted
    :param db_path: The file used to store the data
    """

    with handlers.file_handler(mode='r+', file_path=db_path) as f:
        if not f['action']:
            return {"action": False}

        loaded_data = f["loaded_data"]

    if collection in loaded_data:
        loaded_data.pop(collection)

        with open(db_path, mode='w+', encoding='utf-8') as f:
            json.dump(loaded_data, f, indent=2)

        return {"action": True}

    else:
        return {"action": False, 'message': 'Collection does not exist'}


def generate__id(collection, db_path=DEFAULT_DATABASE_PATH):
    """This function will generate unique _id for the record to be inserted

    :param collection: The collection name
    :param db_path: The file used to store the data
    """
    read_data = read(collection=collection, db_path=db_path)

    if read_data['action']:
        id_count = read_data['matched_count'] + 1
        return {'action': True, '_id': str(uuid.uuid5(uuid.NAMESPACE_URL, str(id_count) + collection + db_path))}

    return {'action': False, 'message': read_data['message']}


def db():
    """This function will return all the databases in 'database' folder
    """

    files = os.listdir('database')

    return files
