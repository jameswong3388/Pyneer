import main
import helpers
import crud


def admin_menu():
    print('--Admin Menu--')
    print('1. Update User\'s info')
    print('2. Delete User')
    print('3. View all Users')
    print('4. Back')
    print('0. Quit')

    option = input('Please select an option >>  ')

    if option == "0":
        main.exit_program()

    elif option == "1":
        update_user_page()

    elif option == "2":
        delete_user_page()

    elif option == "3":
        pass

    elif option == "4":
        main.auth_page()

    else:
        input(main.invalid_input_message)
        admin_menu()


def update_user_page():
    print('--Update User\'s info Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        main.exit_program()

    elif option == "1":
        username = input('Key in the username of the user you want to update: ')

        username_existence = helpers.dictionary_existence_checker(key='username', value=username, table='users')
        print(username_existence)

        if username_existence['validate']:
            key = input('Key in the field you want to update: ')
            value = input('Key in the new value: ')

            data = {"unique_key": "username", "unique_value": username, "key": key, "value": value}

            updated_user = crud.update(file='database.json', table='users', data=data)

            input(updated_user['message'])
            update_user_page()

        else:
            input(username_existence['message'])
            update_user_page()

    elif option == "2":
        admin_menu()

    else:
        input(main.invalid_input_message)
        update_user_page()


def delete_user_page():
    print('--Delete User Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        main.exit_program()

    elif option == "1":
        username = input('Key in the username of the user you want to delete: ')

        username_existence = helpers.dictionary_existence_checker(key='username', value=username, table='users')

        if username_existence['validate']:

            data = {"unique_key": "username", "unique_value": username}

            deleted_user = crud.delete(file='database.json', table='users', data=data)

            input(deleted_user['message'])
            delete_user_page()

        else:
            input(username_existence['message'])
            delete_user_page()

    elif option == "2":
        main.auth_page()

    else:
        input(main.invalid_input_message)
        delete_user_page()
