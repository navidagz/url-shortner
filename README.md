# Url Shortener

Url shortener allows you to create shorter urls obviously :)) <br/>
You have detailed stats and analytics over your urls.

<br>

### TODOs
- [ ] ADD tests

<br>

### Prerequisites
1. `PostgreSQL`
2. `RabbitMQ Server`
3. `Redis`
> If you have docker you can pull `PostgreSQL` and `Redis` and use it (don't forget to publish your ports) 

<br>

### Manual:
1. First of all edit file `.env` in root directory of project and put your credentials there.
2. Make sure you have `python3.6` and `virtualenv` installed
3. Create an virtualenv ```virtualenv venv```
4. Activate venv ```source venv/bin/activate```
5. Create database migrations ```python3.6 manage makemigrations```
6. Migrate database ```python3.6 manage migrate``` 
7. Install requirements  ```pip install -r requirements.txt```
8. Run celery worker ```celery -A url_shortener worker --loglevel=debug ```
9. Run celery beat ```celery -A url_shortener beat --loglevel=DEBUG```
10. Run project ```gunicorn url_shortener.wsgi:application --name="url_shortener" --workers=3 --log-level=debug -b 0.0.0.0:8700```
11. Import Postman collection to see the apis [UrlShortener](https://www.getpostman.com/collections/552044886e3e16075e0c)

<br>

> ### Notes
> 1. Celery beat is used to handle crontab which inserts logs data into database for analytics. This crontab runs every 6 hours (If you want to change it be aware of LOGGING_TIME_ROTATING_INTERVAL)
> 2. Log files will be moved to directory named `analyzed` for further use. 
> 3. Celery worker is used to create logs and handle beat calls
> 4. There is comments for every section of code so feel free to read it.

<br>

### Benchmarks
#### Redirect
```
RRequests: 0, requests per second: 0, mean latency: 0 ms
Requests: 5515, requests per second: 1105, mean latency: 9 ms

Target URL:          http://0.0.0.0:8700/navidagz/
Max time (s):        10
Concurrency level:   10
Agent:               keepalive

Completed requests:  11506
Total errors:        0
Total time:          10.002395444 s
Requests per second: 1150
Mean latency:        8.6 ms

Percentage of the requests served within a certain time
  50%      7 ms
  90%      12 ms
  95%      13 ms
  99%      19 ms
 100%      191 ms (longest request)
Requests: 11506, requests per second: 1198, mean latency: 8.3 ms
```
#### Create ShortUrl
```
Requests: 0, requests per second: 0, mean latency: 0 ms
Requests: 1071, requests per second: 214, mean latency: 46.4 ms

Target URL:          http://0.0.0.0:8700/api/v1/shortener/
Max time (s):        10
Concurrency level:   10
Agent:               keepalive

Completed requests:  2135
Total errors:        0
Total time:          10.003148891 s
Requests per second: 213
Mean latency:        46.6 ms

Percentage of the requests served within a certain time
  50%      44 ms
  90%      58 ms
  95%      63 ms
  99%      81 ms
 100%      197 ms (longest request)
```
> Note:
> 1. Using redis caching helped the redirect response time.
> 2. All analytics process moved to background and only file logging is present in storing redirect log 
> 3. Gunicron is used for WGSI HTTP Server