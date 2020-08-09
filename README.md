# Metrobi Challenges

- I have created a Sanic app with open api documentation using swagger to serve tasks as a simple API.

## Installation

- Clone this repository
- Go to base directory of the repository than create a virtualenvironment with following command `python3 -m venv venv` 
and install requirements `pip install -r requirements.txt` 
- Activate the venv, for Linux or OSX run: `source venv/bin/activate` for windows run: `venv\Scripts\activate.bat`

## Running

- To start sanic, run: `python run.py`, it will start on port http://0.0.0.0:5000/
- Go to swagger docs: http://0.0.0.0:5000/swagger

## Explanation

- I created example app with app factory design pattern and blueprints. Sanic has two blueprints `hello` and `questions`. 
In `__init__.py` file of blueprints module, there is a `create_app()` method which creates and application instance to serve. 
I learnt this pattern while developing Flask applications, which helps me a lot in terms of multiple applications.
[Detailed information about this pattern](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/)