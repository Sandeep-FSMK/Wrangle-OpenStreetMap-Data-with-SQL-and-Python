#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint


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
        
def count_tags(filename):
        # YOUR CODE HERE
    tag_dict= {}    
    for i, elem in enumerate(get_element(filename)):
        if elem.tag not in tag_dict:
            #print(elem.tag) 
            tag_dict[elem.tag] = 1
        else:
            tag_dict[elem.tag] += 1
    
    return tag_dict
            


def test():

    tags = count_tags('bengaluru_india.osm')
    pprint.pprint(tags)
    
    

if __name__ == "__main__":
    test()