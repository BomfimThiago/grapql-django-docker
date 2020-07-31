FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /graphql_django
 WORKDIR /graphql_django
 ADD requirements.txt /graphql_django/
 RUN pip install -r requirements.txt
 ADD . /graphql_django/
 EXPOSE 8000
 