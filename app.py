import auth
import helpers
import crud

if __name__ == "__main__":
    auth.auth_page()

    queried_key = ['username', 'password', 'role']
    read_data = crud.read(file='database.json', table='users', queried_key=queried_key)

    print(read_data)




