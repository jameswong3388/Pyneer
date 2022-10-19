from pages import auth
from api.pyneer import db

if __name__ == "__main__":
    # auth.auth_page()

    a = db.delete_one(collection="asd", select={"username": "admin"})

    print(a)
