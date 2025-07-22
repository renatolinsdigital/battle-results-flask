# Project Setup Guide

## Requirements

- Python 3.6 or higher
- SQLite
- Pipenv

## Setting up the Development Environment

1. **Clone the repository**

   ```bash
   git clone https://github.com/renatolinsdigital/battle-results-flask.git
   cd battle-results-flask
   ```

2. **Create a `.env` file**

   Create a `.env` file in the project's root folder with the following content:

   ```bash
   FLASK_APP=app.py
   FLASK_RUN_HOST=localhost
   FLASK_RUN_PORT=8080
   FLASK_ENV=development
   FLASK_DEBUG=True
   FLASK_SECRET_KEY=my_flask_app_security_key
   LOCAL_DATABASE_PATH=data
   ```

3. **Set up the Python virtual environment**

   ```bash
   # Install pipenv if you don't have it
   pip install pipenv

   # Create a virtual environment
   pipenv --python 3

   # Activate the virtual environment
   pipenv shell

   # Install dependencies
   pipenv install
   ```

4. **Run the application**

   ```bash
   # This will create the database tables and start the server
   python app.py

   # Alternatively, you can use:
   flask run
   ```

5. **Access the application**

   Open your browser and navigate to `http://localhost:8080`

## Development Workflow

1. Activate the virtual environment with `pipenv shell` whenever you start a new development session
2. Make your code changes
3. Run the application with `python app.py` or `flask run`
4. Stop the server with `CTRL+C` when finished
5. Exit the virtual environment with `exit` command

## API Documentation

The API documentation is available at `http://localhost:8080/api/docs` when the application is running.

## Troubleshooting

### Git Command Issues on Windows

If you encounter Git issues on Windows with errors like:

```
fatal: unable to access 'C:\Users\username\.config\git\config': Invalid argument
```

This is often related to path length issues or permission problems on Windows. 

For a complete step-by-step solution to this issue, please refer to our dedicated guide:
[Fixing Git and Virtual Environment Issues on Windows](git_venv_windows_fix.md)

The quick solution is:

1. Set correct environment variables:
   ```bash
   setx HOME %USERPROFILE%
   setx GIT_CONFIG_NOSYSTEM 1
   ```

2. Restart your terminal/command prompt

3. Create a proper `.gitconfig` in your home directory

4. Configure VS Code settings to maintain these environment variables
