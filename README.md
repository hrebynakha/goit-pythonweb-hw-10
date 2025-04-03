# goit-pythonweb-hw-08


Create the .env file

```.env
POSTGRES_PASSWORD=password1
POSTGRES_DB=contacts_app
DEBUG=False
```

Up containers 
```
make up
```
Run migration in docker

```
make migr
```

Up database only
```
make db
```

Run locally (dev mode)
```
make run
```
