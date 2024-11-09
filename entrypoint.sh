#!/bin/bash

# Запуск миграций
alembic upgrade head

# Запуск приложения
python -O main.py
