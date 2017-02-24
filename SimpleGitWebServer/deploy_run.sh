#!/bin/sh
. ./ENV/bin/activate
python deploy_server.py
# export FLASK_APP=deploy_server.py 
# export FLASK_DEBUG=1
# flask run -h 0.0.0.0 -p 54321 --reload > ./deploy_server.log
