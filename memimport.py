#!/usr/bin/env python

import memcache
import json

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
#mc = memcache.Client(['unix:/tmp/memc.sock'])

with open('memdump.json', 'rb') as fp:
        data = json.load(fp)

for key in data.keys():
        mc.set(str(key), str(data[key]))
