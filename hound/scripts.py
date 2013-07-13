# -*- coding: utf-8 -*-

import os
import time
from watchdog.observers import Observer
from docopt import docopt

from .handlers import CoffeeEventHandler
import hound


def hound_cmd():
    """
    Usage:
      hound <path>

    Arguments:
      path          Path to coffescript directory.

    Options:
      -h --help     Show this screen.
      --version     Show version.
    """

    args = docopt(hound_cmd.__doc__, version=hound.__version__)
    run_hound(args['<path>'])


def run_hound(coffee_path):
    coffee_root = os.path.abspath(coffee_path)
    coffee_handler = CoffeeEventHandler(coffee_root=coffee_root)
    observer = Observer()
    observer.schedule(coffee_handler, path=coffee_root, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
