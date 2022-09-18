## Intro
Pyneer is a minimal scaffolding designed to help students with their school's Python assignments. 

Pyneer comes with minimal scaffolding as well as basic authentication and admin functionality to help you quickly get started with your project. It has a well-written API, so you can easily expand and customize your project according to your use case.

Make sure to give it a star if you like the project 👍.

## Requirement
`python` - ^3.8*

## Installation
Make sure you have [`git`](https://git-scm.com/downloads) installed to clone the project directly or manually download it from [`Releases`](https://github.com/jameswong3388/Pyneer/releases)
```
git clone https://github.com/jameswong3388/Pyneer.git
```

## Project Structure
```
.
├── app.py
├── app
│   └── helpers.py
├── api
│   ├── __init__.py
│   └── db
│       └── __init__.py
├── database
│   ├── db.json
│   └── db.txt
└── pages
    ├── admin.py
    ├── auth.py
    └── user.py
```

`index.py` - Here is where Pyneer is initialized.

`\app` - Here contain all of your application logic.

`\api` - Here contain all the API-related files, and all of Pyneer's APIs are here.

`\database` - Here contain the database related file, `db.json` or `db.txt`.

`\pages` - Here contain your pages, and all of Pyneer's scaffolding pages are here.


## API overview
`db.*` - With Pyneer's database API, you can easily execute CRUD operations on your database. Pyneer uses `db.json` as the database file, but you can easily change it when calling the APIs.

## Usage
To run the project, simply run `index.py` with `python` or `python3` depending on your system.
```
python index.py
```


## Bugs and Issues
If you find any bugs or issues, please report it to the [issue tracker](https://github.com/jameswong3388/Pyneer/issues)
