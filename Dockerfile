FROM python:3.6
ADD . /code
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD python3 manage.py migrate
CMD python3 manage.py runserver 127.0.0.1:8000
