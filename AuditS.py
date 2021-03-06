import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "bengaluru_india.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street", 
           "street":"Street",
            "Rd.": "Road",
            "Circle)": "Circle",
            "Cit" : "City",
             "City," : "City",
             "Rd"  : "Road",
             "Road": "Road",
             "Rd." : "Road",
             "stn" : "Station",
             "galli" : "Gali",
            "Layou " :"Layout",
           "layout":"Layout",
           "Layout, ": "Layout",
           "Layout,.": "Layout",
           "main":"Main",
           "MAIN":"Main",
           "Naga":"Nagar",
           "Nagar, ":"Nagar"
           
           }

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
            

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    #for event, elem in ET.iterparse(osm_file, events=("start",)):
    for i, elem in enumerate(get_element(osm_file)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    street_name = []
    street_name = name.split()
    
    #street_name = name.partition(' ')[-1]
    
    if street_name[-1] in mapping.keys():
        name = name.replace(street_name[-1], mapping[street_name[-1]])
    # YOUR CODE HERE
        #print (name)
        #print(street_name)
    return name


def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            #print(st_type)
            better_name = update_name(name, mapping)
            #print name, "=>", better_name
            #if name == "West Lexington St.":
                #assert better_name == "West Lexington Street"
            #if name == "Baldwin Rd.":
                #assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()