#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end':
            yield elem
            root.clear()

def get_user(element):
    return


def process_map(filename):
    users = set()
    user_list = []
    for i, element in enumerate(get_element(filename)):
        if element.attrib.get('uid'):
            #print (element.attrib['uid'])
            user_list.append(element.attrib['uid'])
        
        
        
    users = set(user_list)
    
    #print users
    return users


def test():

    users = process_map('bengaluru_india.osm')
    #pprint.pprint(users)
    print("Total number of users:")
    print(len(users))
    #assert len(users) == 6



if __name__ == "__main__":
    test()