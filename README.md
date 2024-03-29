# Battle Results - Made with Flask

### About this project

This project aims to develop a REST API using Flask + SQLAlchemy for managing game battle results, displaying entries from newest to oldest. The goal is to integrate backend functionality into my game projects and highlight Python code in my portfolio.

### Technologies used

* Sass for styling
* SQLAlchemy as the ORM
* SQLite as the database
* Python as the backend language
* Flask as the backend web framework
* Jinja2 as a template engine for back-end UI rendering

### How it looks after adding a few battle entries

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

# API Endpoints and Models

### The Endpoint /entries:

- **GET - /entries**: Retrieves a list of all finished battle entries.
  
- **POST - /entries**: Enables the creation of a new battle entry using a JSON object in the format of the `BattleEntry` model. Requires unique player names and specifies that the winner's name must match one of the players' names. This request needs a JSON body.

- **GET - /entries/:entryId**: Allows retrieving a specific entry based on the ID provided in the endpoint. For instance, accessing __/entries/1__ will bring the first battle result.

- **DELETE - /entries/:entryId**: Allows deleting a specific entry based on the ID provided in the endpoint. For instance, accessing __/entries/1__ delete the first battle result.

- **PATCH - /entries/:entryId**: Enables updating any field of a battle entry. If names are being updated, the winner's name must be equal to one of the player's names. The only field that cannot be updated is `gameTag` once it represents the specific game in which the battle occurred. This request needs a JSON body as well.

### The model related to battle result entries

Battle Entry model

```js
  {
    id: number, // Auto-generated
    gameTag: string, // required
    player1Name: string, // required
    player2Name: string, // required
    winnerName: string, // required
    finishedDate: string // "YYYY-MM-DD HH:MM:SS" (ISO 8601 standard) - Optional
  }
```

### Data to be received by the /entries endpoint

Example of a JSON body for `POST` requests (Creating a new battle entry)

```json
{
  "gameTag": "dweeb_fight",
  "player1Name": "Player 1",
  "player2Name": "Player 2",
  "winnerName": "Player 2"
}
```

Example of a JSON body for `PATCH` requests (Updating fields of existing entries)

```json
{
  "winnerName": "Player 1"
}
```

