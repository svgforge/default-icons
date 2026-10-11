#!/bin/sh

svgforge -C material.json 'src/material/./**/*.svg'
svgforge --symbol --symbol-render-css --symbol-example \
  --dest='dist/morph' 'src/morph/./**/*.svg'
svgforge -C tango.json 'src/tango/./**/*.svg'
svgforge -C adwaita.json 'src/adwaita/./**/*.svg'

if [ "$1" = "--serve" ]; then
    ./serve.py --dir dist &
    SERVER_PID=$!

    xdg-open "http://localhost:8000"

    wait "$SERVER_PID"
fi
