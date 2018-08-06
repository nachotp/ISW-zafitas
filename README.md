# Proyecto Ingeniería de Software

## Ambiente y ejecución:
El sistema está implementado en Python 3 usando el paquete Django.
Para utilizarlo se debe realizar lo siguiente:
```bash
    python3 -m venv djangoenv
    activate djangoenv
    cd gpiweb
    pip install -r requirements.txt
    python manage.py runserver
```

## Administración
Para hacer commit de cambios en modelo de datos:
```bash
    python manage.py makemigrations
```
Luego para hacerlos efectivos:
```bash
    python manage.py migrate
```
Generar UML
```bash
    python manage.py graph_models -a -X Group,Permission,AbstractUser,LogEntry,ContentType,Session,AbstractBaseSession -o UML.png
```