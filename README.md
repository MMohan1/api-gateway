## What is api-gateway
Design an API Gateway CLI tool, rgate
There is backend services with whom this api getway will connect. 
- Each backend is a container.
- A container is selected as a backend if the container has all the match_labels present as
Docker labels. If there are multiple containers matching, select a random container as a
backend.
- Incoming http requests are routed to the corresponding backend if the path starts with
the given path_prefix.
- If there are no routes matching the request, it should respond with the given body and
status_code in the default_response
- If the backend is down, respond with 503 code
- Accessing http://localhost:8080/stats should give us information about the traffic it
has received so far. An example JSON response is
```{
“requests_count” : {
“success”: 100, // status codes 200-399
“error”: 110, // status codes >399
},
“latency_ms”: {
“average”: 2,
“p95”: 5,
“p99”: 10
}
}
```
## assumptions
1. Not using any data storage. Keeping the request metadata like letency inside application global variable.
2. So if we restart the app the existing data will be lost.
3. Code is easy to extend if tomorrow we want to store request metadata in any datastorage.
4. Docker conatiner is running in local.

## tech
1. [Python3.7](https://www.python.org/downloads/)
2. Flask

## testcase coverage
```
(rgate_venv) mac@macs-mbp rgate % coverage report -m
Name                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------
rgate_app/api.py                            17      8    53%   14-16, 21-23, 28-29
rgate_app/configmanager.py                  22      3    86%   19, 32-33
rgate_app/dockermanager.py                  14      6    57%   19, 23-26, 33
rgate_app/requesthandler.py                 49      2    96%   54, 59
rgate_app/requeststats.py                   29      7    76%   14-16, 33-36
rgate_app/requestwrapper.py                 26      4    85%   33, 37-40
rgate_app/tests/test_configmanager.py       27      0   100%
rgate_app/tests/test_dockermanager.py        5      0   100%
rgate_app/tests/test_requesthandler.py      82      0   100%
rgate_app/tests/test_requeststats.py        34      0   100%
rgate_app/tests/test_requestwrapper.py      12      0   100%
run.py                                      23     23     0%   1-57
----------------------------------------------------------------------
TOTAL                                      340     53    84%
```

## how to install
1. Clone this repo and goinside api-gateway directory (git clone https://github.com/MMohan1/api-gateway.git & cd api-gateway)
2. Install python 3.7.
3. Create venv -> `python3.7 -m venv ../api-gateway_venv`
4. Activate venve `. ../api-gateway_venv/bin/active`
5. Install packages -> `pip install -r requirements.txt`
6. run app -> `python run.py -c /Users/mac/Projects/rgate/config.yml -p 6000` (here -c is for giving the config file path and -p for providing port number)
7. Access the stats api using GET `http://localhost:6000/stats` 
8. Access other api's like `http://localhost:6000/api/payment`
9. Run test cases `nose2 -v rgate_app.tests` 
10. Run test case with coverage `coverage run --source . -m unittest discover -s rgate_app/tests`
11. Get test coverage report `coverage report -m`

## Test With backend conatiner

1. Install Docker
2. Follow this -> https://github.com/MMohan1/python-flask-docker-hello-world
3. Access api `http://localhost:6000/api/payment` you should get response `Flask inside Docker`


