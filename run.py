from app.utils import db
from config import get_env
from app import create_app
from flask_script import Manager
from app.utils.auth import Auth
from app.utils.seed_data import seed_db
from flask_migrate import Migrate, MigrateCommand

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)

# Migrations
manager.add_command('db', MigrateCommand)

@app.before_request
def check_token():
	return Auth.check_token()

@app.before_request
def check_location_header():
	return Auth.check_location_header()

#@app.after_request
#def handle_preflight(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Location')
#    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
#    return response

# Creates the db tables
@manager.command
def create_db():
	db.create_all()

# Drops the db tables
@manager.command
def drop_db():
	db.drop_all()


# seeds database
@manager.command
def seed_all():
	seed_db()


@manager.command
def show_routes():
	from termcolor import colored
	
	count = 0
	for rule in app.url_map.iter_rules():
		methods = [m for m in rule.methods if m in ['GET','POST','PUT','PATCH','DELETE'] ]
		line = 'Method: {method} | Route: {route} | Controller Endpoint: {endpoint}'.format(method=methods[0], route=rule, endpoint=rule.endpoint)
		
		if 'GET' in methods:
			print(colored(line, 'green'), end='\n\n')
			
		if 'POST' in methods:
			print(colored(line, 'yellow'), end='\n\n')
			
		if 'PUT' in methods or 'PATCH' in methods:
			print(colored(line, 'grey'), end='\n\n')
			
		if 'DELETE' in methods:
			print(colored(line, 'red'), end='\n\n')
		
		count+=1
	print(count, 'Routes Found')

if __name__ == '__main__':
	manager.run()
