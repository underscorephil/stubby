#!/bin/sh

HOST=${1:-0.0.0.0}
gunicorn -w 4 -b ${HOST}:4000 stubby.main:app

