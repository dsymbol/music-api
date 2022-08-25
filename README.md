# music-api

REST API created using FastAPI and SQLite3 with a music database 🎵  
SQLAlchemy was not used as I wanted to expand my knowledge of SQL by implementing raw SQL

## Endpoints

#### Artist
![1](https://user-images.githubusercontent.com/88138099/186618519-31a53ce3-85ac-49de-8db2-fb5842d99744.png)

#### Album
![2](https://user-images.githubusercontent.com/88138099/186618701-0b9ec5d5-6619-4e7c-a2a8-025bb94a0ed0.png)

#### Song
![3](https://user-images.githubusercontent.com/88138099/186618740-686d1c8f-de4b-47f1-8199-eb1c894825fa.png)

## Quick Start

Install dependencies:

```bash
git clone https://github.com/dsymbol/music-api
pip install -r requirements.txt
```

Generate database and run the API:

```bash
python src/database.py
python -m uvicorn --port 5000 server:app
```

You can view the API docs by visiting http://localhost:5000

## Example

#### Request:

```
GET http://localhost:5000/api/artist?name=drake
```

#### Response:

```json
[
  {
    "artist_id": 3,
    "name": "Drake",
    "first_name": "Aubrey",
    "last_name": "Graham",
    "phone": "615-541-4518",
    "website": "drakerelated.com",
    "is_group": false
  }
]
```

## PyTest

Tests are independent of each other, database must be reset after every test file ran.
