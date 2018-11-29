#!/bin/sh

# python main.py
gunicorn -b :5000 main:app