#!/usr/bin/env python

import subprocess
import sys
import json
import os
import struct

query = {
    "type": "getLogin",
    "entry": sys.argv[1]
}

querystr = json.dumps(query)

my_env = os.environ.copy()
my_env['PATH'] = '/usr/local/bin:{}'.format(my_env['PATH'])

process = subprocess.Popen(['/usr/local/bin/gopass', 'jsonapi', 'listen'], stdout=subprocess.PIPE, env=my_env, stdin=subprocess.PIPE)
stdout, stderr = process.communicate(input=struct.pack('I', len(querystr))+querystr)
print(json.loads(stdout[4:].strip())[sys.argv[2]])
