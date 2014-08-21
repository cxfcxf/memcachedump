#!/usr/bin/env python

import memcache
import json

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
#mc = memcache.Client(['unix:/tmp/memc.sock'])
mc_server = mc.servers[0]
mc_server.connect()
slabs = []
mc_server.send_cmd('stats items')
keys = []
data = {}


while 1:
        line = mc_server.readline()
        if not line or line.strip() == 'END': break

        item = line.split(' ', 2)

        slab = item[1].split(':', 2)
        slab_id = slab[1]

        if slab_id not in slabs:
                slabs.append(slab_id)


for slab_item in slabs:
        mc_server.send_cmd('stats cachedump %s 0' % slab_item)
        while 1:
                line = mc_server.readline()
                if not line or line.strip() == 'END': break

                item_details = line.split(' ')
                keys.append(item_details[1])

for key in keys:
        data[key] = mc.get(key)

with open('memdump.json', 'wb') as fp:
        json.dump(data, fp)
