Installation steps

Download file "flask_amcef", and place it where you want. 
Right-click on flask_amcef and choose "copy as path".
Clcik on start (windows logo) write "cmd" and open command line.
In command line write "cd <copied path>". cd + space + right click in command line to paste path(NOT ctrl + v).
Next we will check if we have installed python by command "python --version". You should see "Python <version>". If python isn't installed please install it.
Now when we know we have python we can create virtual enviroment. In command line we have to be in path of flask_amcef, something like this "C:\Users\richa\OneDrive\Počítač\projects\flask_amcef>".
In command line we can write command "python -m venv <name_of_your_enviroment>". <name_of_your_enviroment> can be what ever you choose it to be in my case it's called venv.
Now we will activate virtual enviroment by command "venv\Scripts\activate".
Write in cmd "python app.py" to run server.
If it will throw error "ImportError: No module named <name of module>", name of module is any module imported in app.py or forms.py.
Most of the time is good enough copy name of this module and write command "pip install <name of module>".

All pip install modules:
	pip install flask
	pip install SQLAlchemy
	pip install Flask-SQLAlchemy
	pip install flask-login
	pip install flask-bootstrap
	pip install flask-swagger-ui
	pip install Flask-WTF
	pip install WTForms

You can copy all pip installs and just right click in cmd to paste it. You have to be in active virtual enviroment. It will automatically install all modules.
