import time
import re
import datetime

import crud


def null_input_checker(inputs):
    """
    This function will check if the inputs are null.

    (:param) inputs: Inputs in list
    """

    for i in inputs:
        if i == '':
            return {'validate': False, 'message': 'Input cannot be empty.'}
    return {'validate': True, 'message': ""}


def email_input_checker(email):
    """
    This function will check if the email is valid.

    (:param) email: Email in string
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email):
        return {'validate': True, 'message': ""}

    return {'validate': False, 'message': 'Invalid email address'}


def confirm_password_checker(password, confirm_password):
    """
    This function will check if the password and confirm password are the same.

    (:param) password: Password in string
    (:param) confirm_password: Confirm password in string
    """

    if password == confirm_password:
        return {'validate': True, 'message': ""}

    return {'validate': False, 'message': 'Password does not match'}


def birthdate_format_checker(birthdate):
    """
    This function will check if the birthday format is valid.

    (:param) birthdate: Birthday in string in the format of YYYY-MM-DD
    """

    year, month, day = birthdate.split('-')

    print(day, month, year)

    validate = True

    try:
        datetime.datetime(int(year), int(month), int(day))

        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        current_day = datetime.datetime.now().day

        if int(year) > current_year or int(month) > current_month or int(day) > current_day:
            validate = False

    except ValueError:
        validate = False

    if validate:
        return {'validate': True, 'message': "Valid birthdate."}
    else:
        return {'validate': False, 'message': 'Invalid date format.'}


def gender_checker(gender):
    """
    This function will check if the gender was valid.
    (:param) gender: Gender in string
    """

    genders = ['m', 'f', 'M', 'F']

    if gender not in genders:
        return {'validate': False, 'message': "Gender must be (m/f/M/F)."}

    return {'validate': True, 'message': ""}


def processing(process):
    """
    This function will display a processing message.

    (:param) process: An list of string e.g. ['Processing', 'Please wait']
    """

    print()
    for i in process:
        print(i)
        time.sleep(1)
        print()


def existence_checker(key, value, table):
    """
    This function will check if the value of a key exists in the table.

    (:param) key: Dictionary key
    (:param) value: Dictionary value
    (:param) table: Table's name
    """

    read_data = query_object(key=key, value=value, table=table)

    if read_data['status']:
        return {'exist': True, 'message': value + ' existed.'}

    else:
        return {'exist': False, 'message': value + ' does not exist'}


def query_object(key, value, table):
    """
    This function will query the database.json file and return the result.

    (:param) key: Dictionary key
    (:param) value: Dictionary value
    (:param) table: Table's name
    """

    read_data = crud.read(file='database.json', table=table, queried_key=[])

    if read_data['status'] and read_data['result']:
        for data in read_data['result']:

            try:
                if data[key] == value:
                    return {'status': True, 'message': "", 'result': data}

            except KeyError:
                return {'status': False, 'message': 'Key not found'}

            except Exception as e:
                return {'status': False, 'message': str(e)}

            else:
                return {'status': False, 'message': 'Value not found'}

    else:
        return {'status': False, 'message': 'No data found'}


def generate_new_id(table):
    """
    This function will get the last id of the table and add 1 to it.

    (:param) table: The table name
    """

    read_data = crud.read(file='database.json', table=table, queried_key=['id'])

    if read_data['status'] and read_data['result']:
        new_id = read_data['result'][-1]['id'] + 1
        return {'status': True, 'message': "", 'result': new_id}

    else:
        return {'status': False, 'message': 'No data found,'}
