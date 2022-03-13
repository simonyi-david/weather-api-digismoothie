# Weather forecast micro API 

## Installation

Create new virtual environment

    virtualenv env --python=python3.9

Activate environment and install requirements

    source env/bin/activate
    pip install -r requirements.txt

Prepare django related things

    python manage.py migrate
    python manage.py collectstatic

To access admin page on `http://localhost:8000/admin` crate super user

    python manage.py createsuperuser

Then we can start server 

    python manage.py runserver

## Info
When server started we can visit `http://localhost:8000/docs`. There is swagger-ui to easily test endpoints.  

There is only one endpoint - `http://localhost:8000/weather-forecast/`. This endpoint needs two query params `date` and `country_code`

Endpoint returns json as mentioned in the task requirements

Same thing applies also for one custom `manage.py` command. 

    python manage.py weather_forecast <date> <country_code>
    >>> bad | soso | good

This command outputs one of three possible results as described in the task requirements

## Task requirements

Your micro service should fulfil following requirements:

0) It's based on [Django](https://www.djangoproject.com/). You are allowed to use any additional libraries that will help you to finish the task. 

1) It should provide information about weather on following API endpoint

`GET /weather-forecast/?date={YYYY-MM-DD}&country_code={ISO_CODE_2}`

- date is the date of the weather forecast
- country_code is code of the country for which we want to get the forecast. See 3) for more info.

The response should be in JSON format:

```json
{"forecast": "good"}
```

2) It should provide info about weather forecast also via [django management command](https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/#) , eg. `python[manage.py](http://manage.py)weather_forecast 2021-26-05 CZ`

3) Use following simplifications:

- assume that the country_code in exposed interfaces (API, management command) can have only following values: `CZ`, `UK`, `SK`. That means that you're permitted to hard-code eg country_code to GPS coordinates mapping for internal purposes.
- The output of your interfaces will be
    - `good` - in case average temperature on given day is > 20 celsius degrees
    - `soso` - in case average temperature on given dat is between 20 and 10 celsius degrees
    - `bad` - in other cases

4) It's recommended to use [weatherapi.com](https://www.weatherapi.com/) (they provide free Plan that is fully sufficient for purpose of this task) to retrieve info about weather. You can use any other weather provider. But it's mandatory to communicate with some real third party API. 

5) Our service should be fast and efficient. That means that we don't want to delegate repeated requests to weatherapi.com. It's recommended to use some internal storage (database).