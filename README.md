# omnialatamtest
API for operations on Ecomerce flow

### Software requirements
* Python 3.9
* Django
* Django REST framework
* flake8

### Project execution

Poject can be executed with docker-compose

```bash
# Executes
 docker-compose up -d
```

Once the project its executed Swagger docs can be seen in:

[http://127.0.0.1:72/swagger-docs/]

To consume service first must be an user created this operation can be performed on [http://127.0.0.1:72/users/create/],
once user creation a auth token can be requested at [http://127.0.0.1:72/users/token] and all others operations must be consumed
with **Authorization Token** header.


### Run Tests

Test may be executed with

```bash
python manage.py test
```

### Test coverage

Coverage was generated by coverage package and can be found in: 

[Coverage](ecomerceflow/htmlcov/index.html)

## Disclaimers

- For windows systems the volume mapping on database doesn't work well so it's better to quit the line when running the compose app
