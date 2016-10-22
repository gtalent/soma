from python:latest

env PYTHONUNBUFFERED 1

#run apt-get update
#run apt-get install -y nginx
run mkdir /code
workdir /code
add requirements.txt /code/
run pip install -r requirements.txt
add . /code/

expose 8000

cmd ["./manage.py", "runserver", "0.0.0.0:8000"]
