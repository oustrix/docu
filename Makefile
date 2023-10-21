deps:
	pip install -r requirements.txt
run:
	export FLASK_APP=app; export FLASK_DEBUG=true; flask run --port 8080
