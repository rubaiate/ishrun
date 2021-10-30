#!/usr/bin/python3

import subprocess
import os

last_cmd = os.path.join(os.environ['ISH_RUN_SCRIPTS'], 'ish_last_cmd')
if os.path.isfile(last_cmd):
    with open(last_cmd) as ish_last:
        cmd = ish_last.readline().strip()
        print(cmd)
        subprocess.call(cmd.split(' '))
