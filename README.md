# todo_flask

## Front-end & Back-end Todo list

To start with this project:

 1. Clone it to your desktop:
 
	`git clone https://github.com/Muhaymin21/todo_flask.git`

 3. Install requirements:
 
	`pip install -r requirements.txt`

 4. Create .env file and add all of this variables:

	```
	DB_DIALECT=<Example postgresql>
	DB_USER=<Example postgres>
	DB_PASSWORD=<Example 12345>
	DB_HOST=<Example localhost>
	DB_PORT=<Default 5432>
	DB_NAME=<Example postgres>
	APP_DEBUG=<0 for False and 1 for True>
	```

 5. Create tables:

	```
	flask db init
	```
	```
	flask db migrate
	```
	```
	flask db upgrade
	```

 6. Run the app:
 
	`Python app.py`
