#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Here, the XML first is processed programmatically. Each line is read in via a sax-parser (xml.etree.cElementTree). 
Elements are added according to the schema provided (see example below). Cleaning steps are performed programmatically.
Finally, the cleaned content is written out in a json file (later to be added to a MongoDB instance).

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
		  "version":"2",
		  "changeset":"17206049",
		  "timestamp":"2013-08-03T16:43:42Z",
		  "user":"linuxUser16",
		  "uid":"1219059"
		},
"pos": [41.9757030, -87.6921867],
"address": {
		  "housenumber": "5157",
		  "postcode": "60625",
		  "street": "North Lincoln Ave"
		},
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from update_functions import *

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
lower = re.compile(r'^([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def shape_element(element):

	"""
	Iterates through .xml file. Reshapes fields according to chosen schema.
	Performs programmatic auditing and cleaning. Converts and writes out file to 
	.json format.
	"""

	node = {}
	# Processing only "node" or "way" tags:
	if element.tag == "node" or element.tag == "way":
		node['type'] = element.tag

		# Creating 'created' field:
		if 'version' or 'changeset' or 'timestamp' or 'user' or 'uid' in element.attrib:
			node['created'] = {}

		# Creating 'pos' array with latitude/longitude info for geospatial indexing:
		if 'lat' and 'lon' in element.attrib:
			node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
		
		# Iterating over first-level attribute data:
		for attribute in element.attrib:
			if attribute in CREATED:
				node['created'][attribute] = element.attrib[attribute]
			elif attribute == 'lat' or attribute == 'lon':
				continue
			else:
				node[attribute] = element.attrib[attribute]

		# Iterating over second-level tags:
		for subtag in element.iter():
			# Processing 'tag' tags:
			if subtag.tag == "tag":
				# Ignoring address info with more than one colon:
				if len(subtag.attrib['k'].split(":")) > 2 and 'addr' in subtag.attrib['k']:
					continue
				# Ignoring keys with problem characters:
				elif problemchars.search(subtag.attrib['k']):
					continue
				# Adding address info in 'address' dict:
				elif 'addr:' in subtag.attrib['k']:
					if "address" not in node.keys():
						node["address"] = {}
					try:
						key = subtag.attrib['k'].split(":")[1]
						node["address"][key] = subtag.attrib['v']
					except:
						continue
						# A problem occurred in cases where the field 'address' already exists (with the entire address as a string)
						# For completeness of information, the existing address info is retained (could be parsed as a future improvement)
				else:
					node[subtag.attrib['k']] = subtag.attrib['v']
			# Processing 'nd' tags:
			elif subtag.tag == "nd":
				if not "node_refs" in node.keys():
					node["node_refs"] = [subtag.attrib['ref']]
				else:
					node["node_refs"].append(subtag.attrib['ref'])
			# Processing remaining data:
			else:
				for attr in subtag.attrib:
					if attr not in CREATED + ['lat', 'lon']:
						node[attr] = subtag.attrib[attr]

			### Performing cleaning steps:

			# Updating phone number format:
			if node.get("phone"):
				node["phone"] = update_phone(node["phone"])

			# Turns field "contact:phone" into "phone" and updates if field "phone" does not exist:
			if node.get("contact:phone") and not node.get("phone"):
				node["phone"] = update_phone(node["contact:phone"])

			# Turning shops into amenities (cf. update_functions.py for details):
			if node.get("shop"):
				node = update_shop(node)

		element.clear() # for better memory usage
		# See: https://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree
		return node
	else:
		return None


def process_map(file_in, pretty = False):
	file_out = "{0}.json".format(file_in)
	with codecs.open(file_out, "w") as fo:
		for _, element in ET.iterparse(file_in):
			el = shape_element(element)
			if el:
				if pretty:
					fo.write(json.dumps(el, indent=2)+"\n")
				else:
					fo.write(json.dumps(el) + "\n")

osm_file = ""
# local path to osm_file needs to be specified above

if __name__ == '__main__':
	process_map(osm_file, False)


