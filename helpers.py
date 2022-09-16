import time
import re
import crud


def null_input_checker(inputs):
    for i in inputs:
        if i == '':
            return {'validate': False, 'message': 'Input cannot be empty,'}
    return {'validate': True, 'message': ""}


def email_input_checker(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email):
        return {'validate': True, 'message': ""}

    return {'validate': False, 'message': 'Invalid email address,'}


def confirm_password_checker(password, confirm_password):
    if password == confirm_password:
        return {'validate': True, 'message': ""}

    return {'validate': False, 'message': 'Password does not match,'}


def birthday_format_checker(birthday):
    regex = r'\d{4}-\d{2}-\d{2}'

    if re.fullmatch(regex, birthday):
        return {'validate': True, 'message': ""}

    return {'validate': False, 'message': 'Invalid birthday format,'}


def gender_checker(gender):
    genders = ['m', 'f', 'M', 'F']

    if gender not in genders:
        return {'validate': False, 'message': "Gender must be (m/f/M/F),"}

    return {'validate': True, 'message': ""}


def processing(process):
    print()
    for i in process:
        print(i)
        time.sleep(1)
        print()


def dictionary_existence_checker(key, value, table):
    read_data = crud.read(file='database.json', mode='r', table=table, queried_key=[key])

    found = False

    if read_data['status'] and read_data['result']:
        for data in read_data['result']:
            if data[key] == value:
                found = True

                return {'validate': True, 'message': ""}

        if not found:
            return {'validate': False, 'message': "Value Not found,"}

    else:
        return {'validate': False, 'message': 'No data found,'}
