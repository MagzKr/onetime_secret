#!/bin/bash
docker-compose up -d
sleep 5
alembic upgrade head
