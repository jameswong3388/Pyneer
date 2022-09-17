import auth
import helpers
import crud

invalid_input_message = "Invalid input, press enter to try again . . ."


def admin_menu():
    print('--Admin Menu--')
    print('1. Update User\'s info')
    print('2. Delete User')
    print('3. View all Users')
    print('4. Back')
    print('0. Quit')

    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        update_user_page()

    elif option == "2":
        delete_user_page()

    elif option == "3":
        pass

    elif option == "4":
        auth.auth_page()

    else:
        input(invalid_input_message)
        admin_menu()


def update_user_page():
    print('--Update User\'s info Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        user_id = int(input('Key in the "ID" of the user you want to update: '))

        user_id_existence = helpers.existence_checker(key='id', value=user_id, table='users')

        if user_id_existence['exist']:
            key = input('Key in the field you want to update: ')
            value = input('Key in the new value: ')

            data = {"unique_key": "id", "unique_value": user_id, "key": key, "value": value}

            updated_user = crud.update(file='database.json', table='users', data=data)

            input(updated_user['message'])
            update_user_page()

        else:
            input(user_id_existence['message'])
            update_user_page()

    elif option == "2":
        admin_menu()

    else:
        input(invalid_input_message)
        update_user_page()


def delete_user_page():
    print('--Delete User Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        user_id = int(input('Key in the "ID" of the user you want to delete: '))

        user_id_existence = helpers.existence_checker(key='id', value=user_id, table='users')

        if user_id_existence['exist']:

            data = {"unique_key": "id", "unique_value": user_id}

            deleted_user = crud.delete(file='database.json', table='users', data=data)

            input(deleted_user['message'])
            delete_user_page()

        else:
            input(user_id_existence['message'])
            delete_user_page()

    elif option == "2":
        auth.auth_page()

    else:
        input(invalid_input_message)
        delete_user_page()
