# Pyneer

## Intro
Pyneer is a framework designed to help students with their school's Python project, especially Beginners level  and that's why is called Pyneer.

Pyneer comes with simple scaffolding as well as basic authentication, and admin functionality to help you get started with your project.
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
├── api
│   ├── crud.py
│   ├── database.py
│   └── helpers.py
├── database
│   ├── db.json
│   └── db.txt
└── pages
    ├── admin.py
    ├── auth.py
    └── user.py
```

`app.py` - The main file to run the project.

`\api` - Contains all the API related files, most of your app's logic will be here.

`\database` - Contains the database file, you can use `db.json` or `db.txt` to store your data.

`\pages` - Contains all the pages, feel free to extend it.

## Usage
To run the project, simply run `app.py` with `python` or `python3` depending on your system.
```
python app.py
```