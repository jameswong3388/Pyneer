import auth
import crud


if __name__ == "__main__":
    # auth.auth_page()

    data = {}

    a = crud.delete(file="database.json", table="testing", data=data)

    print(a)
