#!/bin/sh

# starts the crawljax webapp
host=127.0.0.1
proxy_port=8008
port=$1
SCRIPTNAME=$0

BASEDIR=$(dirname "$SCRIPTNAME")
cd $BASEDIR

#java -Dhttp.proxyHost=${host} -Dhttp.proxyPort=${proxy_port} -jar crawljax-web-3.6.jar -p ${port} -o ${output_folder}
exec java -jar "${BASEDIR}/crawljax-web-3.6.jar" -p ${port} > ajax_crawl.log 2>&1

