import crud
import helpers
import admin

invalid_input_message = "Invalid input, press enter to try again . . ."
empty_input_message = "Please enter a value . . ."


def auth_page():
    print('--Authentication Page--')
    print('1. Login')
    print('2. Register')
    print('0. Quit')
    print()
    option = input('Please select an option > ')

    if option == "0":
        exit_program()
    elif option == "1":
        login_page()
    elif option == "2":
        register_page()
    else:
        input(invalid_input_message)
        auth_page()


def login_page():
    print('--Login Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        exit_program()

    elif option == "1":
        username = input('Username: ')
        password = input('Password: ')

        validation = helpers.null_input_checker([username, password])

        if validation['validate']:
            authenticator(username, password)

        else:
            input(validation['message'])
            login_page()

    elif option == "2":
        auth_page()

    else:
        input(invalid_input_message)
        login_page()


def register_page():
    print('--Register Page--')
    print('1. Continue')
    print('2. Back')
    print('0. Quit')
    print()
    option = input('Please select an option >>  ')

    if option == "0":
        exit_program()

    elif option == "1":
        print('--Registration--')
        username = input('Username: ')
        password = input('Password: ')
        confirm_password = input('Confirm Password: ')
        email = input('Email: ')
        gender = input('Gender (m/f/M/F): ')
        gender = gender.lower()
        birthdate = input('Birthday (YYYY-MM-DD): ')

        empty_validation = helpers.null_input_checker([username, password, confirm_password, email, gender, birthdate])

        username_validation = helpers.existence_checker(key='username', value=username, table='users')

        password_validation = helpers.confirm_password_checker(password, confirm_password)

        email_validation = helpers.email_input_checker(email)

        gender_validation = helpers.gender_checker(gender)

        birthday_format_validation = helpers.birthday_format_checker(birthdate)

        if empty_validation['validate'] and email_validation['validate'] and password_validation['validate'] and \
                not username_validation['exist'] and birthday_format_validation['validate'] and \
                gender_validation['validate']:

            new_user_id = helpers.get_new_id(table='users')

            register({"id": new_user_id['result'], "username": username, "password": password,
                      "email": email, "gender": gender, "birthday": birthdate, "role": "user"})
        else:

            validation_messages = [
                empty_validation['message'],
                username_validation['message'],
                password_validation['message'],
                email_validation['message'],
                gender_validation['message'],
                birthday_format_validation['message']
            ]

            print(validation_messages)

            for message in validation_messages:
                print(message)
                input('Press enter to try again . . .')
                register_page()

    elif option == "2":
        auth_page()

    else:
        input(invalid_input_message)
        register_page()


def main_menu(user_info):
    print('--Main Menu--')
    print(user_info)
    exit_program()


def authenticator(auth_username, auth_password):
    authenticate = False

    queried_key = ['username', 'password', 'role']
    read_data = crud.read(file='database.json', table='users', queried_key=queried_key)

    if read_data['status'] and read_data['result']:
        for user in read_data['result']:
            if auth_username == user['username'] and auth_password == user['password']:
                authenticate = True
                helpers.processing(['Logging in . . .', 'Welcome, {}!'.format(user['username'])])
                if user['role'] == 'admin':
                    admin.admin_menu()
                else:
                    main_menu(user)

        if not authenticate:
            print('Invalid username or password')
            login_page()

    else:
        print(read_data['message'])
        login_page()


def register(inputs):
    process = crud.create(file='database.json', table='users', data=inputs)

    if process['status']:
        helpers.processing(['Registering . . .', 'Registration successful!'])
        login_page()
    else:
        helpers.processing(['Registering . . .', 'Registration failed!'])
        register_page()


def exit_program():
    helpers.processing(['Exiting program . . .', 'Goodbye!'])
    exit()


if __name__ == '__main__':
    # auth_page()

    a = crud.delete_table(table='a')

    print(a)
