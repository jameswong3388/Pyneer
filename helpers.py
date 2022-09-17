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


def birthdate_format_checker(birthdate):
    """
    This function will check if the birthday format is valid.

    (:param) birthdate: Birthday in string in the format of YYYY-MM-DD
    """

    year, month, day = birthdate.split('-')

    validate = True

    try:
        datetime.datetime(int(year), int(month), int(day))

        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        current_day = datetime.datetime.now().day

        if len(month) != 2 or len(day) != 2:
            validate = False

        if int(year) >= int(current_year):
            if int(month) >= int(current_month):
                if int(day) > int(current_day):
                    validate = False

    except ValueError:
        validate = False

    if validate:
        return {'validate': True, 'message': "Valid birthdate."}
    else:
        return {'validate': False, 'message': 'Invalid date format.'}


def age_calculator(birthdate):
    """
    This function will calculate the age of the user.

    (:param) birthdate: Birthday in string in the format of YYYY-MM-DD
    """

    year, month, day = birthdate.split('-')

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day

    age = current_year - int(year)

    if int(month) > current_month:
        age -= 1

    elif int(month) == current_month:
        if int(day) > current_day:
            age -= 1

    return age


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


def exit_program():
    processing(['Exiting program . . .', 'Goodbye!'])
    exit()


def existence_checker(key, value, table, file='database.json'):
    """
    This function will check if the value of a key exists in the table.

    (:param) key: Dictionary key
    (:param) value: Dictionary value
    (:param) table: Table's name
    """

    read_data = query(key=key, value=value, table=table, file=file)

    if read_data['status'] and read_data['result']:
        for data in read_data['result']:
            if data[key] == value:
                return {'exist': True, 'message': '"' + str(value) + '" existed.'}

    else:
        return {'exist': False, 'message': 'value "' + str(value) + '" does not exist.'}


def query(key, value, table, file='database.json'):
    """
    This function will query the database.json file and return a result
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
        return {'status': False, 'message': 'No data found'}
