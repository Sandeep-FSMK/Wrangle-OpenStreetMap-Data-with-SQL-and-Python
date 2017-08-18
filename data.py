#!/usr/bin/env python
# -*- coding: utf-8 -*-



import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema
import AuditS
import AuditZ


OSM_PATH = "bengaluru_india.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    def write_node():
    
        node_attribs['id'] = element.attrib['id']
        node_attribs['user'] = element.attrib['user']
        node_attribs['uid'] = element.attrib['uid']
        node_attribs['version'] = element.attrib['version']
        node_attribs['lat'] = element.attrib['lat']
        node_attribs['lon'] = element.attrib['lon']
        node_attribs['timestamp'] = element.attrib['timestamp']
        node_attribs['changeset'] = element.attrib['changeset']
        #node_main_dict['node'] =node_dict
    
        #print(node_main_dict)
        
        for child in element:
            
            elem_dict={}
            if child.tag == 'tag':
                     
                
                elem_dict['id'] =element.attrib['id']
                
                #inter_string=child.attrib['k']
                #print(child.attrib) 
                if 'k' in child.attrib:
                    s = PROBLEMCHARS.search(child.attrib['k'])
                    if not s:
                        
            
                    
                        m = LOWER_COLON.search(child.attrib['k'])
                        #commenting the below line to use the regular expression
                        #if ':' not in child.attrib['k']:
                        if not m:
                            
                            elem_dict['key'] =child.attrib['k']
                            elem_dict['type']='regular'
                        else:
                            key_list= child.attrib['k'].split(':',1)
                        #print(key_list)
                            elem_dict['key'] = key_list[-1]
                            elem_dict['type']=key_list[0]
                        if((child.attrib['k'] =='addr:postcode') or (child.attrib['k'] =='addr:zipcode') ) :
                            
                            
                            name=AuditZ.update_zipcode(child.attrib['v'])
                            #if (name!=child.attrib['v']):
                            #print(name)
                            #print(child.attrib['v'])
                            
                            
                        elif (child.attrib['k'] =='addr:street'):
                            
                            name=AuditS.update_name(child.attrib['v'], AuditS.mapping)
                        else:
                            name = child.attrib['v']
                            
                             
                        
                        elem_dict['value'] = name
                    
                        
                        tags.append(elem_dict)
        
        #node_main_dict['node_tag']=tags
        #print({'node': node_attribs, 'node_tags': tags})
    def write_way():
    
        way_attribs['id'] = element.attrib['id']
        way_attribs['user'] = element.attrib['user']
        way_attribs['uid'] = element.attrib['uid']
        way_attribs['version'] = element.attrib['version']
        way_attribs['timestamp'] = element.attrib['timestamp']
        way_attribs['changeset'] = element.attrib['changeset']
        #node_main_dict['way'] =node_dict
        iteration = 0 
        
        #print(node_main_dict)
        
        for child in element:
            
            elem_dict={}
            
            #iteration+=1
            if child.tag == 'nd':
                
                
                elem_dict['id'] =element.attrib['id']
                elem_dict['node_id'] = child.attrib['ref']
                elem_dict['position']= iteration
                way_nodes.append(elem_dict)
                iteration+=1
                
            if child.tag == 'tag':
                elem_dict={}
                     
                
                elem_dict['id'] =element.attrib['id']
                 
                
                
                if 'k' in child.attrib:
                    s = PROBLEMCHARS.search(child.attrib['k'])
                    if not s:
                        
            
                    
                        m = LOWER_COLON.search(child.attrib['k'])
                        #commenting the below line to use the regular expression
                        #if ':' not in child.attrib['k']:
                        if not m:
                            
                            elem_dict['key'] =child.attrib['k']
                            elem_dict['type']='regular'
                        else:
                            key_list= child.attrib['k'].split(':',1)
                        #print(key_list)
                            elem_dict['key'] = key_list[-1]
                            elem_dict['type']=key_list[0]
                        if((child.attrib['k'] =='addr:postcode') or (child.attrib['k'] =='addr:zipcode') ) :
                            
                            
                            name=AuditZ.update_zipcode(child.attrib['v'])
                            #if (name!=child.attrib['v']):
                            #print(name)
                            #print(child.attrib['v'])
                            
                            
                        elif (child.attrib['k'] =='addr:street'):
                            
                            name=AuditS.update_name(child.attrib['v'], AuditS.mapping)
                        else:
                            name = child.attrib['v']
                            
                             
                        
                        elem_dict['value'] = name
                    
                        
                        tags.append(elem_dict)
        
        #print ("sorry")
        #print({'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags})    
        
    if element.tag == 'node':
        write_node()
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        write_way()
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    pass
                    #validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
