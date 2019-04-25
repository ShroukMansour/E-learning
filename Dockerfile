FROM python:3.6
ADD . /code
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD python3 manage.py migrate
CMD python3 manage.py runserver 0.0.0.0:8000
