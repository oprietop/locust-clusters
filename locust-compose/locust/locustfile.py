#! /usr/bin/python
# -*- coding: utf8 -*-

from locust import HttpLocust, TaskSet, task, events
from stats import stats

# Pump resources
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

class Postman_TaskSet(TaskSet):
    def on_start(self):
        self.client.get("/basic-auth", auth=('postman', 'password'))

    @task(1)
    def Get(self):
        self.client.get("/get?test=123")

    @task(1)
    def Post(self):
        self.client.post("/post", {"one": 1, "two": 2})


class MyLocust(HttpLocust):
    host = 'https://postman-echo.com'
    task_set = Postman_TaskSet
    min_wait = 10000
    max_wait = 30000    # Initialize the influxDB stats and hooks on the master

if '--master' in sys.argv:
    s = stats()

    # Initialize and run the stats reporting
    def start_reporting():
            s.start()

    # Stop the stats reporting
    def stop_reporting():
         s.stop()
            
    # Hook the functions into events
    events.master_start_hatching += start_reporting
    events.master_stop_hatching += stop_reporting
