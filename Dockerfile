from python:latest

env PYTHONUNBUFFERED 1

run mkdir /code
workdir /code
add requirements.txt /code/
run pip install -r requirements.txt
add . /code/

cmd ["./manage.py", "runserver", "0.0.0.0:8000"]
