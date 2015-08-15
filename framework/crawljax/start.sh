#!/bin/sh

# starts the crawljax webapp
host=127.0.0.1
proxy_port=8008
port=$1
curr_dir=${PWD}

#java -Dhttp.proxyHost=${host} -Dhttp.proxyPort=${proxy_port} -jar crawljax-web-3.6.jar -p ${port} -o ${output_folder}
java -jar ${curr_dir}/framework/crawljax/crawljax-web-3.6.jar -p ${port}

