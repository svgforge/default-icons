#!/bin/sh

svgforge -C config.json ./**/*.svg

./serve.py --dir OUT/symbol &
SERVER_PID=$!

xdg-open "http://localhost:8000"

wait "$SERVER_PID"
