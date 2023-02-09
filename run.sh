#!/bin/bash

CURRENT_DIR=`pwd`
PORT=3008

echo "Compiling syntax analysis proj..."
cd $CURRENT_DIR/src/syntax_analysis/recursive_descent
go build -o runnable
if [ $? != 0 ]; then
    echo "Compiling failed!" 1>&2
    exit 1
fi
echo "Deploying..."
sudo kill -9 $(sudo lsof -t -i:$PORT)
cd $CURRENT_DIR/src/coordinator_webserver
nohup node server.js > log.out &

echo "Done!"
