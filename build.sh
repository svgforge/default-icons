#!/bin/sh

svgforge -C material.json  'material/./**/*.svg'
svgforge -C tango.json  'tango/./**/*.svg'

./serve.py --dir dist &
SERVER_PID=$!

xdg-open "http://localhost:8000"

wait "$SERVER_PID"
