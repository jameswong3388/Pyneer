# Pyneer

## Intro
Pyneer is a minimal scaffolding designed to help students with their school's Python project, especially for people who just started learning Python.


Pyneer comes with minimal scaffolding as well as basic authentication, and admin functionality to help you get started with your project. It has well written api , so you can be easily expand and customized according to your use case.

Makesure give it a star if you like the project 👍.

## Requirement
`python` - ^3.8*

## Installation
Make sure you have `git` installed to clone the project directly or manually download from `Releases`
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
│   ├── crud.py
│   └── database.py
├── database
│   ├── db.json
│   └── db.txt
└── pages
    ├── admin.py
    ├── auth.py
    └── user.py
```

`app.py` - The main file to run the project.

`\app` - Here contains all your application logic.

`\api` - Contains all the API related files, all the Pyneer's API are here.

`\database` - Contains the database file, you can use `db.json` or `db.txt` to store your data.

`\pages` - Contains all the pages, feel free to extend it.

## Usage
To run the project, simply run `index.py` with `python` or `python3` depending on your system.
```
python index.py
```


## Bugs and Issues
If you find any bugs or issues, please report it to the [issue tracker](https://github.com/jameswong3388/Pyneer/issues)
