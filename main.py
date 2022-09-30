from pages import auth
from api import db
from api import handlers
import json

if __name__ == "__main__":
    # auth.auth_page()

    select = {"email": "admin@localhost"}
    update = {'key': "asd", 'value': "test"}
    collection = 'asd'
    file_path = 'database/db.json'
    data = [{"name": "test", "age": 20}, {"name": "test2", "age": 30}]

    a = db.update_one(select=select, update=update, collection=collection, file_path=file_path)
    print(a)

    # with handlers.file_handler(mode='r', file_path=file_path) as f:
    #     if f['message']:
    #         print(f['message'])
    #
    #     loaded_data = f['loaded_data']
    #
    # try:
    #     if isinstance(select, dict) and isinstance(update, dict) and update != {}:
    #         a = db.query(field=select, data=loaded_data[collection])
    #         if a['acknowledge']:
    #             for i in a['result']:
    #                 for key, value in update.items():
    #                     i[key] = value
    #
    #                 break
    #
    #             with open(file_path, 'w+') as f:
    #                 f.seek(0)
    #                 json.dump(loaded_data, f, indent=2)
    #
    #             print('Updated')
    #
    #         else:
    #             print('Not found')
    #
    #     else:
    #         print('Action failed.')
    #
    # except KeyError:
    #     print('Collection not found.')
