#!/bin/bash
docker-compose up -d
wait 5
alembic upgrade head
