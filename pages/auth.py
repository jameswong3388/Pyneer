from api import crud, helpers, database
from pages import user, user as user_page, admin

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
        helpers.exit_program()
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
        helpers.exit_program()

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
        helpers.exit_program()

    elif option == "1":
        print('--Registration--')

        inputs = ['Email: ', 'Gender (m/f/M/F): ', 'Birthdate (YYYY-MM-DD): ']

        validation_method = [helpers.email_input_checker, helpers.gender_checker, helpers.birthdate_format_checker]

        new_id = database.generate_new_id(table='users')

        validated_inputs = {"id": new_id['result']}

        while True:
            username = input('Username : ')
            username_validation = helpers.existence_checker(key='username', value=username, table='users')

            if not username_validation['exist'] and username != '':
                validated_inputs['username'] = username
                break

            else:
                print("Username already exist or Invalid Input")
                continue

        while True:
            password = input('Password : ')
            confirm_password = input('Confirm Password: ')

            password_validation = helpers.null_input_checker([password, confirm_password])

            if password == confirm_password and password_validation['validate']:
                validated_inputs['password'] = password
                break

            else:
                print("Password does not match or Invalid Input")
                continue

        for i in inputs:
            while True:
                user_input = input(i)

                not_null = user_input != ''

                validation = validation_method[inputs.index(i)](user_input)

                if validation['validate'] and not_null:
                    validated_inputs[inputs[inputs.index(i)].split(' ')[0].lower()] = user_input
                    break

                else:
                    print(validation['message'], 'or Invalid Input')
                    continue

        age = helpers.age_calculator(validated_inputs['birthdate'])
        validated_inputs['age'] = age

        register(validated_inputs)

    elif option == "2":
        auth_page()

    else:
        input(invalid_input_message)
        register_page()


def authenticator(auth_username, auth_password):
    authenticate = False

    queried_key = ['username', 'password', 'role']
    read_data = crud.read(table='users', queried_key=queried_key)

    if read_data['status'] and read_data['result']:
        for data in read_data['result']:
            if auth_username == data['username'] and auth_password == data['password']:
                authenticate = True
                helpers.processing(['Logging in . . .', 'Welcome, {}!'.format(data['username'])])
                if data['role'] == 'admin':
                    admin.admin_menu()
                else:
                    user_page.main_menu(data)

        if not authenticate:
            print('Invalid username or password')
            login_page()

    else:
        print(read_data['message'])
        login_page()


def register(inputs):
    process = crud.create(table='users', data=inputs)

    if process['status']:
        helpers.processing(['Registering . . .', 'Registration successful!', 'Redirecting to login page . . .',
                            'Welcome, {}!'.format(inputs['username'])])
        user.main_menu(inputs)
    else:
        helpers.processing(['Registering . . .', 'Registration failed!'])
        register_page()
