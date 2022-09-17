from pages import auth
import api
from app import helpers

invalid_input_message = "Invalid input, press enter to try again . . ."


def admin_menu():
    print('--Admin Menu--')
    print('1. Modify/Update Table\'s objects')
    print('2. Delete Table\'s objects')
    print('3. View Table\'s objects')
    print('4. Create new Table')
    print('5. Back')
    print('0. Quit')

    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        update_object()

    elif option == "2":
        delete_object()

    elif option == "3":
        view_table()

    elif option == "4":
        pass

    elif option == "5":
        auth.auth_page()

    else:
        input(invalid_input_message)
        admin_menu()


def update_object():
    print('--Modify/Update Table\'s objects--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":

        while True:

            table = input('Key in the table you want to update: ')
            input_id = input('Key in the "ID" of the user you want to update: ')

            existence = helpers.existence_checker(key='id', value=input_id, table=table)

            if existence['exist']:
                break

            else:
                input('ID or table does not exist, press enter to try again . . .')
                continue

        key = input('Key in the field you want to update: ')
        value = input('Key in the new value: ')

        data = {"unique_key": "id", "unique_value": input_id, "key": key, "value": value}
        updated_user = api.update(table='users', data=data)

        input(updated_user['message'])
        update_object()

    elif option == "2":
        admin_menu()

    else:
        input(invalid_input_message)
        update_object()


def delete_object():
    print('--Delete User Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        while True:

            table = input('Key in the table you want to delete from: ')
            input_id = input('Key in the "ID" of the user you want to delete: ')

            existences = helpers.existence_checker(key='id', value=input_id, table=table)

            if existences['exist']:
                break

            else:
                input('ID or table does not exist, press enter to try again . . .')
                continue

        data = {"unique_key": "id", "unique_value": input_id}
        deleted_user = api.delete(table=table, data=data)

        input(deleted_user['message'])
        delete_object()

    elif option == "2":
        auth.auth_page()

    else:
        input(invalid_input_message)
        delete_object()


def view_table():
    print('--View all Users Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        users = api.read(table='users', queried_key=[])

        for user in users['result']:
            print(user)

        input('Press enter to continue . . .')
        admin_menu()

    elif option == "2":
        admin_menu()

    else:
        input(invalid_input_message)
        view_table()
