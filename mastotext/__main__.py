import logging

import argh

from mastotext.main import main

logging.basicConfig(level=logging.DEBUG)
argh.dispatch_command(main)
