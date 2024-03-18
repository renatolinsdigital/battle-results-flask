# Battle Results - Made with Flask

### About this project

This project aims to develop a REST API using Flask + SQLAlchemy for managing game battle results, displaying entries from newest to oldest. The goal is to integrate backend functionality into my game projects and highlight Python code in my portfolio.

# Technologies used

* Sass for styling
* SQLAlchemy as the ORM
* SQLite as the database
* Python as the backend language
* Flask as the backend web framework
* Jinja2 as a template engine for back-end UI rendering

# How it looks after adding a few battle entries

![Print](prints/print.png)

---

# Running and coding in this project

* Create a `.env` file in the project's root folder. For development purposes, it will work fine if you fill it like this:

  ```js
  FLASK_APP=app.py
  FLASK_RUN_HOST=localhost
  FLASK_RUN_PORT=8080
  FLASK_ENV=development
  FLASK_DEBUG=True
  FLASK_SECRET_KEY=my_flask_app_security_key
  LOCAL_DATABASE_PATH=data
  ```

* Have SQLite installed on your machine. You can check the official SQLite website and follow the installation instructions.
* Install Pipenv on your machine with `pip install pipenv`.
* Create a virtual environment with `pipenv --python 3`.
* Activate/reactivate a virtual environment associated to this project with `pipenv shell`.
* Confirm virtual environment creation path with `pipenv --venv`.
* Install project's dependencies using `pipenv install`.
* Run this project with `python app.py` to make sure the data base Path + URI are going to be resolved. After that, you can run this app with `flask run`.
* Open your browser and check the project running with `localhost:8080`.
* Make desired updates as you wish, this project is fully open source.

Once you have completed your coding session, you can stop the development server by pressing `CTRL + C` and exit the virtual environment by using the `exit` command.

---

## Endpoints and params:

- **GET - /entries**: Brings total number of battle entries
  
- **GET - /entries/page={page_number}**: Brings battle results for a given page. First pages show last entries

- **GET - /entries/id={id}**: Bring a specific battle result for a given id

- **GET - /entries/between/start={start_date}&end={end_date}**: Bring battle results for a given data range

- **GET - /entries/gametag={game_tag}**: Brings battle results for a given game tags, as this application can be used for many games.

- **POST - /entries**: Allows the creation of a new battle entry once a JSON (in Battle entry model format) is provided. Player names must be unique within each game tag

- **PUT - /entries/id={id}**: Allows updating winner´s player name of a specific battle entry. Useful if one wants to keep the same name across different games

## Models

### Battle entry model

```js
  {
    gameTag: string,
    player1Name: string,
    player2Name: string,
    winnerName: string,
    finishedDate: string // YYYY-MM-DD HH:MM:SS (ISO 8601 standard)
  }
```

### Battle entry JSON example (You can send this JSON using Insomnia with a POST request for testing the API)

```json
{
  "gameTag": "dweeb_fight",
  "player1Name": "Player 1",
  "player2Name": "Player 2",
  "winnerName": "Player 2",
  "finishedDate": "2024-03-25 10:30:50"
}
```

