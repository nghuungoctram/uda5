Getting Started
Installing Dependencies
Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

Initialize and activate a virtualenv using:
python -m virtualenv env
source env/bin/activate
Note - In Windows, the env does not have a bin directory. Therefore, you'd use the analogous command shown below:


PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

pip install -r requirements.txt
Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy and Flask-SQLAlchemy are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in ./src/database/models.py. We recommend skimming this code first so you know how to interface with the Drink model.

jose JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

Configure Environment Variables
Open .env file and change each variable appropriately to your desired environment

Running the server
Each time you open a new terminal session, run:

export FLASK_APP=app.py;
To run the server, execute:

flask run --reload
The --reload flag will detect file changes and restart the server automatically.

Permissions
App API permissions:

get:shirt - create a new shirt
post:shirt - create a new shirt
patch:shirt - update a new shirt by id
delete:shirt - delete a new shirt by id

get:customer - create a new customer
post:customer - create a new customer
patch:customer - update a new customer by id
delete:customer - delete a new customer by id

manage:categories - including create, update, delete category

can post:shirt
can patch:shirt
can delete:shirt

can post:customer
can patch:customer
can delete:customer
