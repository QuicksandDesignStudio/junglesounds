# Setup
- Setup virtual env `python3 -m junglesounds_venv`
- Activate `source junglesounds_venv/bin/activate`
- Install `pip install -r requirements`

# Setup db
- `python3 manage.py db upgrate`


# Start 
- Start `python3 manage.py run`


# Dev 
- In dev all the app specific data will be in data folder. In production it will be outside the project path
- data/dev.db is the database
- data/sample_audio is the sample audio folder - in prod it will be S3
- data/predict_audio is the audio folder which users have sent for prediction. This is not done yet

# Web
 All the web is defined inside the  `controller - application.py`. All the static files for the standard web - say images and js are in static folder. All the html templates are in templates folder

 On dev the web is at http://localhost:5000/

# Gunicorn
gunicron -w 4 manage:app -b 127.0.0.1:5000

# API

## User

We have not added an API to this yet. PLease add to the DB directly. As of now its not used for anything special. There are already two users 
```
1- thejeshgn
2- romit
```

## Category

### Add category

- POST <base_url>/api/categories

Parameters

- category=Elephant
- slug=elephant

### Get all categories

- GET <base_url>/api/categories


### Get a single category

- GET <base_url>/api/category/<category_id>


## Sample

### Add Sample

- POST <base_url>/api/samples

Parameters

- sample_audio=Multipart audio file


### Get all Samples

- GET <base_url>/api/samples

Parameters

```
- no_of_reviews = how many classification reviews this sample has had. If you want to classifiy the freshly uploaded one, use 0. Default is None. it gets all
- per_page = how many to get per page, default 20
- page = which page
```



```
{
    "samples": [
        {
            "id": 3,
            "sample_file_name": "3.wav",
            "classifications": [],
            "file_hash": "3",
            "no_of_reviews": 0,
            "recorded_time": null,
            "recorded_location": null
        },
        {
            "id": 4,
            "sample_file_name": "5cbefa05-852c-4d63-81f8-9f5478ff7449.wav",
            "classifications": [],
            "file_hash": "8aef8bfe22c0ac432687548b01667884",
            "no_of_reviews": 0,
            "recorded_time": "Thu, 26 May 2016 11:42:00 -0000",
            "recorded_location": "Bangalore"
        }
    ],
    "pagination": {
        "has_next": true,
        "has_prev": true,
        "page": 2,
        "per_page": 2,
        "pages": 4,
        "total": 7
    }
}
```

And

- If the API retunes only the file name `sample_file_name`
- Actual file url will be <base_url>/api/download<sample_file_name>


### Get a single sample

- GET <base_url>/api/sample/<sample_id>



## Classification
### Add Classification

- POST <base_url>/api/classifications

Parameters

```
- sample_id = Integer ID
- user_id = Integer ID
- category_id = Integer ID
- start_time = Float
- end_time = Float
- recorded_time = Format %Y-%m-%dT%H:%M:%S.%f%z like 2016-05-26T11:42:00.56+0530 
- recorded_location = Sting
```

### Get all Classification

- GET <base_url>/api/classifications


Parameters

```
- per_page = how many to get per page, default 20
- page = which page
```

```
{
    "classifications": [
        {
            "id": 1,
            "user": {
                "id": 2,
                "username": "romit"
            },
            "sample": {
                "id": 1,
                "sample_file_name": "36c0a8d3-875d-48a2-ae85-8afae8234473.wav",
                "no_of_reviews": 1,
	            "recorded_time": "Thu, 26 May 2016 11:42:00 -0000",
    	        "recorded_location": "Bangalore"
            },
            "category": {
                "id": 0,
                "category": null,
                "slug": null
            },
            "start_time": 9.55,
            "end_time": 8.66
        }
    ],
    "pagination": {
        "has_next": false,
        "has_prev": false,
        "page": 1,
        "per_page": 20,
        "pages": 1,
        "total": 1
    }
}
```

And

- If the API retunes only the file name `sample_file_name`
- Actual file url will be <base_url>/api/download<sample_file_name>


### Get a single sample

- GET <base_url>/api/classification/<classification_id>



## Prediction
- Yet to be done
