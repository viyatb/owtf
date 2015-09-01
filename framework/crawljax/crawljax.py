#!/usr/bin/python2
from __future__ import print_function
import os
import signal
import json
import logging
from framework.dependency_management.dependency_resolver import BaseComponent
from framework.dependency_management.interfaces import CrawljaxInterface
import urllib2


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
            print("[*] Please run the setup script again")
        # check if enabled by the user
        if self.db_config.Get("AJAX_CRAWL") == "True":
            self.is_initiated = 1
        self.interface = self.db_config.Get("CRAWLJAX_INTERFACE")
        self.port = self.db_config.Get("CRAWLJAX_PORT")



    @staticmethod
    def check_dependency():
        # check if the lib/ is populated and crawljax_web.jar is present or not
        jar = os.path.join(RootDir, "crawljax-web-3.6.jar")
        lib_dir = os.path.join(RootDir, "lib/")
        if jar and os.listdir(lib_dir):
            return True
        else:
            return False

    @staticmethod
    def stop():
        """ checks if Crawljax is running in the background or not
            if it is, then stop the process and clean-up
        """
        # check if crawljax is running
        for line in os.popen("ps ax | grep crawljax-web-3.6.jar | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)

    def start(self):
        try:
            self.start = os.system("sh %s %s %s &" % (script, self.interface, self.port))
            print("[*] Crawljax web interface started on http://%s:%s" % (self.interface, self.port))
        except:
            print("Cannot initiate Crawljax")
            logging.warn("Cannot initiate Crawljax")


    def scan(self, config):
        print("[*] Sending config data now...")
        config_post = "http://%s:%s/rest/configurations/" % (self.interface, self.port)
        start_scan = "http://%s:%s/rest/history/" % (self.interface, self.port)

        # post the config
        conf_json = json.dumps(config)
        config_create = urllib2.Request(config_post)
        config_create.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(config_create, conf_json)
        if response.getcode() == 200:
            # now start the scan
            start_scan_req = urllib2.Request(start_scan)
            start_scan_req.add_header('Content-Type', 'application/json')
            scan_res = urllib2.urlopen(start_scan_req, config["name"])
            if scan_res.getcode() == 200:
                print("[*] Crawljax scan started...")
            else:
                print("[*] There was an error.")

