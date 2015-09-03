#!/usr/bin/python2
from __future__ import print_function
import os
import signal
import logging
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

