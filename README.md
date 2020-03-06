# README

## Getting started with the homieassistant

1. Find replace `homieassistant` with your project name
2. Rename the `./homieassistant` and `./homieassistant/homieassistant` folders
3. Remove this section from the README
4. Start coding!

## Starting the project locally

1. Set up local `.env` file containing at least the env vars seen in sample file below.
2. `docker-compose build`
3. `docker-compose up -d`

Example `.env` working with the current local docker-compose setup:

```
ENV=LOCAL
DEBUG=True

STATIC_ROOT=/var/www/homieassistant-static/
MEDIA_ROOT=/var/www/homieassistant-media/

DB_PASSWORD=supersecret
SECRET_KEY=loremipsumdolorsitamet
```

## Setting up the first admin user

1. `make createsuperuser email=my-email@example.com`

Note that the email has to be valid when calling make to get a valid one-time-use token!
Else you can call addstatictoken directly with:
 `make addstatictoken email=my-email@example.com`

## Testing

1. Make sure the project is running locally
2. `make test`

See the makefile for additional arguments and shortcuts.

## Deploying

## Infrastructure
