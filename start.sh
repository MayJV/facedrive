#!/bin/bash
python3.6 manage.py
# python3 projects/manage.py celery worker -l info --concurrency=20 &
# python3 projects/manage.py celery beat -l info