#!/usr/bin/python2
import sys
import os
import signal
import subprocess
from framework.dependency_management.dependency_resolver import BaseComponent
from framework.dependency_management.interfaces import CrawljaxInterface


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
            print "Please run the setup script again"
        self.init()
        self.is_initiated = 0 #if above passes, then set to 0

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
    def init():
        """ checks if Crawljax is running in the background or not
            if it is, then stop the process and clean-up
        """
        # check if crawljax is running
        pid = os.system("ps -ef | grep crawljax-web-3.6.jar | awk '{print $2}'")
        if pid:
            try:
                os.kill(pid, signal.SIGKILL)
            except:
                print "No such process"

    def start(self):
        print script
        try:
            os.system("sh "+script+" 4444")
            # set initiated var to 1
            self.is_initiated = 1
        except:
            print "Cannot start Crawljax"

    def stop(self):
        # simply reuse the init function
        self.init()

