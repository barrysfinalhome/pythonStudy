#!/bin/sh
exec /usr/bin/ssh -v -o StrictHostKeyChecking=no -i /home/barry.ye/.ssh/id_rsa "$@"
