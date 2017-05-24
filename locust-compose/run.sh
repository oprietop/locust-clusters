#!/bin/sh
docker-compose down
docker-compose up -d
docker-compose scale locust-slave=4
docker-compose logs --follow
