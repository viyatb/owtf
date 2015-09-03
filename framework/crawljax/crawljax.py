#!/usr/bin/python2
from __future__ import print_function
import os
import signal
import json
import logging
import urllib2
from framework.dependency_management.dependency_resolver import BaseComponent
from framework.dependency_management.interfaces import CrawljaxInterface
from framework.utils import FileOperations


RootDir = os.path.dirname(os.path.abspath(__file__))
script = os.path.join(RootDir, "start.sh")


class Crawljax(BaseComponent, CrawljaxInterface):
    """
    Initialises the crawljax plugin, and sets up the required configuration
    """
    COMPONENT_NAME = "crawljax"


    def __init__(self):
        self.register_in_service_locator()
        self.config = self.get_component("config")
        self.db_config = self.get_component("db_config")
        self.target = self.get_component("target")
        self.db = self.get_component("db")
        if not self.check_dependency():
            logging.info("Please run the setup script again")
        # check if enabled by the user
        if self.db_config.Get("AJAX_CRAWL") == "True":
            self.is_initiated = 1
        # get the interface and port for crawljax
        self.interface = self.db_config.Get("CRAWLJAX_INTERFACE")
        self.port = self.db_config.Get("CRAWLJAX_PORT")
        # create the dirs if not already
        self.crawljax_dir = os.path.join(self.config.RootDir, self.config.FrameworkConfigGet("OUTPUT_PATH"), 'misc', 'crawljax')
        FileOperations.create_missing_dirs(self.crawljax_dir)

    @staticmethod
    def check_dependency():
        """
        :rtype: boolean
        """
        # check if the lib/ is populated and crawljax_web.jar is present or not
        jar = os.path.join(RootDir, "crawljax-web-3.6.jar")
        lib_dir = os.path.join(RootDir, "lib/")
        if jar and os.listdir(lib_dir):
            return True
        else:
            return False

    @staticmethod
    def stop():
        """
        Checks if Crawljax is running in the background or not if it is, then stop the process and clean-up
        """
        # check if crawljax is running
        for line in os.popen("ps ax | grep crawljax-web-3.6.jar | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)

    def start(self):
        """
        Starts the Crawljax app with specified interface and port
        """
        try:
            self.start = os.system("sh %s %s %s &" % (script, self.interface, self.port))
            logging.warn("Crawljax web interface started on http://%s:%s" % (self.interface, self.port))
        except:
            logging.warn("Cannot initiate Crawljax")


    def scan(self, config):
        """
        Scan intiator using Crawljax's rest api
        :param config: config dict
        :type config: dict
        :rtype: boolean
        """
        conf = config
        logging.info("Sending config data now...")
        config_post = 'http://%s:%s/rest/configurations/' % (self.interface, self.port)
        start_scan = 'http://%s:%s/rest/history/' % (self.interface, self.port)

        # post the config
        conf_json = json.dumps(conf)
        config_create = urllib2.Request(config_post, conf_json)
        config_create.add_header('Content-Type', 'application/json')
        conf_res = urllib2.urlopen(config_create)
        if conf_res.code == 200:
            # now start the scan
            start_scan_req = urllib2.Request(start_scan, conf["name"].replace('.', '-'))
            start_scan_req.add_header('Content-Type', 'text/plain')
            scan_res = urllib2.urlopen(start_scan_req)
            if scan_res.code == 200:
                logging.info("Crawljax scan started...")
                return True
            else:
                logging.info("There was an error.")
                return False

