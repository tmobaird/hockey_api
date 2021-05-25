### Running Tests

```
python manage.py test
```

**Games module only**

```bash
python manage.py test games
```

### Updating dependencies

Install Package

```bash
pip install <package>
```

Generate requirements file
```bash
pip freeze > requirements.txt
```

Update Pipenv from requirements.txt
```bash
pipenv -r requirements.txt
```