import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "bengaluru_india.osm"

zipcode_re = re.compile(r'560\d\d\d', re.IGNORECASE) #zipcode according to mumbai

#find if there is whitespace in the zip code ; then search for pattern. and add it			
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
            

def audit_zip_code(zip_types,zipcode):
    #remove any whitespace from the string
    if (' ' in zipcode) == True:
        #print zipcode
        zip_types[zipcode].add(zipcode)
        
        
    #search for the pattern of zipcode
    m = zipcode_re.search(zipcode)
    if not m:
        
        zip_types[zipcode].add(zipcode)
        #print zipcode

def is_zip_code(elem):
    return ((elem.attrib['k'] == 'addr:postcode')  or (elem.attrib['k'] == 'addr:zipcode') ) 

def audit(osmfile):
    osm_file = open(osmfile, "r")
    zip_types = defaultdict(set)
    #for event, elem in ET.iterparse(osm_file, events=("start",)):
    for i, elem in enumerate(get_element(osm_file)):

        if elem.tag == "node" or  elem.tag == "way":
            for tag in elem.iter("tag"):
                
                if is_zip_code(tag):
                    #print(tag.attrib['v'])
                    audit_zip_code(zip_types,tag.attrib['v'])

    return zip_types



def update_zipcode(zipcode):
    m = zipcode_re.search(zipcode)
    
    if not m:
        #print zipcode        
        zipcode = zipcode.replace(' ' ,'') #remove whitespace in between
        zipcode = zipcode.replace('o', '0') #replace o with zeros
        
        #replace the 2 digit zipcodes with complete 
        j=re.search('[a-zA-Z]', zipcode)
        if len(zipcode )== 2: #special case for 2 digits zip code.
            #print zipcode
            zipcode = '5600' + zipcode 
        elif len(zipcode) !=6 and not j:
            #print zipcode
            #get the last 3 chars 
            zipcode = '560' + zipcode[-3:]
            print zipcode
        
    return zipcode

def test():
    zip_types = audit(OSMFILE)
    #   assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    #change st_types with zip_types here when using zip code
    for zip_types,ways in zip_types.iteritems():
    #for st_type, ways in st_types.iteritems():
        for name in ways:
            #better_name = update_name(name, mapping)
            better_zip = update_zipcode(name)
            

                        
            #print name, "=>", better_name
            #print name, "=>", better_zip
            

if __name__ == '__main__':
    test()
        
        
    