## Notes API
Notes API where you can assign and view its tags

## Installation
Create a virtual environment
```shell
pip install virtualenv
virtualenv venv
```

Run virtual environtment(Windows)
```shell
venv\Scripts\activate
```

For Linux/MacOS
```shell
source env/bin/activate
```

Install requirements

```shell
pip install -r requirements.txt
```

To create the db
```shell
python src/adapter/schema.py
```

To start the server, run:

```shell
uvicorn src.router.app:app --reload
```

For docs of available API go to http://127.0.0.1:8000/docs
