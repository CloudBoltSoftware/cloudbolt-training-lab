# Cloudbolt Training Lab
This app is a collection of lab resources that will accompany a guide to instruct the user various parts of CloudBolt. 




# Pre-requsites:

postgres running locally 
- [download Postgres](https://www.postgresql.org/download/)

# Developing Locally
To get the resource running locally, perform the following steps:

    createdb cloudbolt_training_lab -U postgres --password 

Export the database URL to your environment variables:

    export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/cloudbolt_training_lab

Apply migrations:

    python manage.py migrate

Start the app:

    python manage.py runserver 0.0.0.0:8000


# Extending the app
This app is built using Django Cookie Cutter to make use of Django best practices and consistent documentation. 

To extend this app in any manner, consult the django cookie cutter documentation: https://django-cookiecutter.readthedocs.io/en/latest/

## Included apps:

### Cars
This app exposes three API endpoints for creating cars. 
- Manufacturer (/cars/api/manufacturer/)
- Make (/cars/api/ars/)
- Trim (/cars/api/trim)
