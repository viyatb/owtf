#!/bin/sh

# starts the crawljax webapp
host=127.0.0.1
proxy_port=8008
interface=$1
port=$2
SCRIPTNAME=$0

BASEDIR=$(dirname "$SCRIPTNAME")
cd $BASEDIR

exec java -Djetty.host=${interface} -Dhttp.proxyHost=${host} -Dhttp.proxyPort=${proxy_port} -jar "${BASEDIR}/crawljax-web-3.6.jar" -p ${port} > ajax_crawl.log 2>&1

