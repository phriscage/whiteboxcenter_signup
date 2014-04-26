#!/usr/bin/env python

import sys
import logging

sys.path.append('/usr/local/whiteboxcenter_signup/lib')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s[%(process)s] : %(funcName)s : %(message)s',
    filename='/var/log/whitebox/api.whitebox.center.log'
)
from whitebox.v1.api.main import create_app
#from main import create_app
application = create_app()
