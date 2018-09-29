#!/usr/bin/env bash

get_container_ip() {
     export PROXY_HOST=`hostname -i | awk '{print $1}'`
}

case "${1}" in
  start_dns )
    get_container_ip
    python main.py
  ;;
  bash )
    /bin/bash
  ;;
  *)
    echo "specify a command. start_dns or bash"
  ;;
esac
