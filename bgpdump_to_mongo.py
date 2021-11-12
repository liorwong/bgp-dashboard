#! /usr/bin/env python3

import sys
import json
import pymongo
import ipaddress
from datetime import datetime

def db_connect(host="mongodb"):
    client = pymongo.MongoClient(host=host)
    return client.bgp

def initialize_database(db):
    """Create indxes, and if the db contains any entries set them all to 'active': False"""
    # db.bgp.drop()
    db.bgp.create_index('nexthop')
    db.bgp.create_index('nexthop_asn')
    db.bgp.create_index([('nexthop', pymongo.ASCENDING), ('active', pymongo.ALL)])
    db.bgp.create_index([('nexthop_asn', pymongo.ASCENDING), ('active', pymongo.ALL)])
    db.bgp.create_index([('ip_version', pymongo.ASCENDING), ('active', pymongo.ALL)])
    db.bgp.create_index([('origin_asn', pymongo.ASCENDING), ('ip_version', pymongo.ASCENDING), ('active', pymongo.ALL)])
    db.bgp.create_index([('communities', pymongo.ASCENDING), ('active', pymongo.ALL)])
    db.bgp.create_index([('as_path.1', pymongo.ASCENDING), ('nexthop_asn', pymongo.ASCENDING), ('active', pymongo.ALL)])
    db.bgp.update_many(
        {"active": True},  # Search for
        {"$set": {"active": False}})  # Replace with

def dump_line_to_json(line):
    try:
        items = line.split("|")
        # print(items)
        as_path = items[6].split(" ")
        update_json = {
            '_id': items[5],
            'ip_version': ipaddress.ip_address(items[5].split('/', 1)[0]).version,
            'origin_asn': int(as_path[-1]),
            'nexthop': items[8],
            'nexthop_asn': int(as_path[0]), 
            'as_path': as_path,
            'med': items[10],
            'local_pref': items[9],
            'communities': items[11].split(" "),
            'route_origin': items[7],
            'atomic_aggregate': items[12],
            'aggregator_as': None, # TODO: not implemented yet
            'aggregator_address': None, # TODO: not implemented yet
            'originator_id': None, # TODO: not implemented yet
            'cluster_list': [], # TODO: not implemented yet
            'withdrawal': False,
            'age': datetime.fromtimestamp(int(items[1])).strftime('%Y-%m-%d %H:%M:%S ') + 'UTC',
            'active': True,
            'history': [], # TODO: not implemented yet
        }
        if items[2] == "W": # withdrawal
            update_json["withdrawal"] = True
            update_json['active'] = False
        
        return update_json

    except:
        print("ERROR in %s" % line)

def main():
    db = db_connect()
    initialize_database(db)
    for line in sys.stdin:
        prefix_from_bgpdump = dump_line_to_json(line)
        db.bgp.update({"_id": prefix_from_bgpdump['_id']}, prefix_from_bgpdump, upsert=True)

if __name__ == "__main__":
    sys.exit(main())
