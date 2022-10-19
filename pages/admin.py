from pages import auth
from api.pyneer import db
from app import helpers

invalid_input_message = "Invalid input, press enter to try again . . ."


def admin_menu():
    print('--Admin Menu--')
    print('1. Modify/Update Collection\'s documents')
    print('2. Delete Collection\'s documents')
    print('3. View Collection\'s documents')
    print('4. Create new Collection')
    print('5. Back')
    print('0. Quit')

    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        update_document()

    elif option == "2":
        delete_document()

    elif option == "3":
        view_collection()

    elif option == "4":
        create_new_collection()

    elif option == "5":
        auth.auth_page()

    else:
        input(invalid_input_message)
        admin_menu()


def update_document():
    print('--Modify/Update Collection\'s documents--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":

        while True:

            collection = input('Key in the collection you want to update: ')
            input_id = input('Key in the "ID" of the user you want to update: ')

            existence = helpers.existence_checker(key='id', value=int(input_id), collection=collection)

            if existence['exist']:
                break

            else:
                input('ID or collection does not exist, press enter to try again . . .')
                continue

        key = input('Key in the field you want to update: ')
        value = input('Key in the new value: ')

        select = {"key": "id", "value": int(input_id)}
        updated_user = db.update_one(collection='users', select=select, update={"key": key, "value": value})

        if updated_user['action']:
            input('User updated successfully, press enter to continue . . .')
            admin_menu()
        else:
            input('User update failed, press enter to continue . . .')
            update_document()

    elif option == "2":
        admin_menu()

    else:
        input(invalid_input_message)
        update_document()


def delete_document():
    print('--Delete Collection\'s objects--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        while True:

            collection = input('Key in the collection you want to delete from: ')
            input_id = input('Key in the "ID" of the user you want to delete: ')

            existences = helpers.existence_checker(key='id', value=int(input_id), collection=collection)

            if existences['exist']:
                break

            else:
                input('ID or collection does not exist, press enter to try again . . .')
                continue

        data = {"unique_key": "id", "unique_value": int(input_id)}
        deleted_user = db.delete_one(collection=collection, select=data)

        if deleted_user['action']:
            input('User deleted successfully, press enter to continue . . .')
            admin_menu()

        else:
            input('User delete failed, press enter to continue . . .')
            delete_document()

    elif option == "2":
        auth.auth_page()

    else:
        input(invalid_input_message)
        delete_document()


def view_collection():
    print('--View Collection\'s objects--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        users = db.read(collection='users', query=[])

        for user in users['result']:
            print(user)

        input('Press enter to continue . . .')
        admin_menu()

    elif option == "2":
        admin_menu()

    else:
        input(invalid_input_message)
        view_collection()


def create_new_collection():
    print('--Create new Collection--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        helpers.exit_program()

    elif option == "1":
        collection = input('Key in the name of the collection you want to create: ')
        created_table = db.create_collection(collection=collection)

        if created_table['action']:
            input('Collection created successfully, press enter to continue . . .')
            admin_menu()

        else:
            input('Collection creation failed, press enter to continue . . .')
            create_new_collection()

    elif option == "2":
        admin_menu()

    else:
        input(invalid_input_message)
        create_new_collection()
