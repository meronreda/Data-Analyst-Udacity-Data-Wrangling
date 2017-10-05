import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import csv
import codecs
import cerberus
import schema

#!/usr/bin/env python
# -*- coding: utf-8 -*-
OSM_FILE = "las-vegas_nevada.osm"  # Replace this with your osm file
OSM_PATH = OSM_FILE
SAMPLE_FILE = "sample.osm"

k = 10 # Parameter: take every k-th top level element

OSMFILE = OSM_FILE
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Lane", "Road",
            "Parkway"]

# these were some of the street abreviations found when I did the audit, I will be changing the common ones to make it more standard 
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "AVE": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "Ln": "Lane",
            "Ln.": "Lane",
            "blvd": "Boulevard",
            "blvd.": "Boulevard",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Pkwy": "Parkway",
            "Cir" : "Circle",
            "Mt.": "Mountain",
            "Dr" : "Drive"
            }


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
osm_file = open(OSM_FILE, "r")

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)



# I first ran code on a sample file below before running on my actual osm file for quicker code processing
def openmyfile(file):
    with open(SAMPLE_FILE, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')

        # Write every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write('</osm>')


def get_element(SAMPLE_FILE, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(OSM_FILE, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename, events=("start", "end")):
        if event == 'start':
            if elem.tag in tags:
                tags[elem.tag] += 1
            #if it doesn't exist yet that means you need to add a new key and set the count to 1
            else:
               tags[elem.tag] = 1
    return tags

def test():

    tags = count_tags(OSM_FILE)
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 4328,
                     'nd': 1181889,
                     'node': 994412,
                     'osm': 1,
                     'relation': 558,
                     'tag': 574228,
                     'way': 102846}

def test2():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map(OSM_FILE)
    pprint.pprint(keys)
    assert keys == {'lower': 300441, 'lower_colon': 265414, 'other': 8373, 'problemchars': 0}                     



def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Your task is to explore the data a bit more.
Before you process the data and add it into your database, you should check the
"k" value for each "<tag>" and see if there are any potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""




def key_type(element, keys):
    elem_key = 'other'
    if element.tag == "tag":
        k = element.get('k')
        if lower.search(k):
            elem_key = 'lower'
        if lower_colon.search(k):
            elem_key = 'lower_colon'
        if problemchars.search(k):
            elem_key = 'problemchars'

        #print element.get('k'), element.get('v')
        #print k
        #print '\t', elem_key
        keys.setdefault(elem_key, 0)
        keys[elem_key] += 1

    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        uname = element.get('user')
        if uname is not None:
            users.add(uname)


    return len(users)


"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""




def get_element(OSM_FILE, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(OSM_FILE, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def audit_street_type(street_types, street_name):
    #print "******************"
    #print street_name
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

#if postcode matches 5 digits, return. if not, add to postcodes dict
def audit_postcode(postcodes, postcode):
    postcodes[postcode].add(postcode)
    return postcodes

def audit(osmfile):
    print osmfile
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcodes = defaultdict(set)
    for i, elem in enumerate(get_element(osmfile)):
    #for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_postcode(tag):
                    postcodes = audit_postcode(postcodes, tag.attrib['v'])
    osm_file.close()
    pprint.pprint(dict(postcodes))
    pprint.pprint(len(street_types))

    return street_types, postcodes

street_types, postcodes = audit(OSMFILE)

def update_postcode(postcode):

    #searches for postcodes that match desired of 5 digits
    search = re.match(r'^\d{5}$',postcode)
    #searches for postcodes that start w/abbrev. state name 
    search2 = re.match(r'^[NV].{2}(\d{5})',postcode)
    #searches for postcodes that start with the state name
    search3 = re.match(r'^[a-zA-z].{6}(\d{5})',postcode)
    #searches for postcodes that have a 4 digit code after
    search4 = re.match(r'^(\d{5})-\d{4}$', postcode)

    
    if search:
        clean_postcode = search.group()
        # returns `clean_postcode` and exits function
        return clean_postcode
    elif search2:
        clean_postcode = search2.group(1)
        return clean_postcode
    elif search3:
        clean_postcode = search3.group(1)
        return clean_postcode
    elif search4:
        clean_postcode = search4.group(1)
        return clean_postcode

for postcode in postcodes:
    print postcode.encode("utf-8")
    print "updated"
    print update_postcode(postcode)
    print "--------"
    

def update_name(name, mapping):
    unexpected = street_type_re.search(name)

    if not unexpected:
        return name

    unexpected = unexpected.group()
    if unexpected not in mapping:
        return name
    replacement = mapping[unexpected]

    better_name = re.sub(unexpected, replacement, name)
    #print len(better_name)
    return better_name
    #print better_name


def assert_stname():
    #st_types = audit(OSM_FILE)
    assert len(street_types) == 66
    pprint.pprint(dict(street_types))

    for street_type, ways in street_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "S Rainbow Blvd":
                assert better_name == "S Rainbow Boulevard"



if __name__ == "__main__":
    openmyfile("las-vegas_nevada.osm")
    #audit("las-vegas_nevada.osm")
    process_map("las-vegas_nevada.osm")
    test()
    test2()

