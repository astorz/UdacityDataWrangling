import xml.etree.cElementTree as ET
import pprint
import re

# osm_file = ""
# local path to osm_file needs to be specified 


# Auditing phone numbers

def audit_phone():
	"""
	Identifies phone numbers that do not conform to the chosen standard
	(+International calling code, followed only by numbers, 
	e.g. +49123456789).
	"""

	for _, elem in ET.iterparse(osm_file):

		phones_inconsistent = set()
		regex_phone = r'^\+49\d+$'

		for tag in elem.iter():
			try:
				if tag.attrib["k"] == "phone":
					if not re.search(regex_phone, tag.attrib["v"]):
						phones_inconsistent.add(tag.attrib["v"])
					else:
						continue
			except:
				continue
	pprint.pprint(phones_inconsistent)

if __name__ == "__main__":
	audit_phone()

##########################################################################
##########################################################################

# Auditing shops

def audit_shop():

	"""
	Identifies and counts distinct types of shops.
	"""

	shops = {}

	for _, elem in ET.iterparse(osm_file):

		for tag in elem.iter():
			try:
				items = tag.items()
				if items[0][0] == 'k' and items[0][1] == 'shop':

					shop = items[1][1]

					if shop not in shops:
						shops[shop] = 1
					else:
						shops[shop] += 1
			except:
				continue

	pprint.pprint(shops)
if __name__ == "__main__":
	audit_shop()

##########################################################################
##########################################################################


# Auditing zip codes

def audit_postcode():

	"""
	Identifies and prints all postal codes that do not conform to 
	the standard, i.e. consisting only of 5 digits.
	"""

	unique_postcodes = set()

	regex_postcode = r'^\d{5}$'

	for _, elem in ET.iterparse(osm_file):

		for tag in elem.iter():
			try:
				if tag.attrib["k"] == "addr:postcode":
					m = re.match(regex_postcode, tag.attrib["v"])
					if not m:
						unique_postcodes.add(tag.attrib["v"])
			except:
				continue

	pprint.pprint(sorted(unique_postcodes))

if __name__ == "__main__":
	audit_postcode()

##########################################################################

def audit_postcode_berlin():

	"""Tests whether a postcode is in Berlin.
	Valid postcodes range from 10115-14199 
	(http://www.postleitzahlen-berlin.com/).
	"""

	count_berlin = 0
	count_non_berlin = 0
	non_berlin = set()

	for _, elem in ET.iterparse(osm_file):

		for tag in elem.iter():
			try:
				if tag.attrib["k"] == "addr:postcode":
					if not 10115 <= int(tag.attrib["v"]) <= 14199:
						count_non_berlin += 1
						non_berlin.add(tag.attrib["v"])
					else:
						count_berlin += 1
			except:
				continue
	
	pprint.pprint(non_berlin)
	print('Count Berlin: ' + str(count_berlin))
	print('Count Non-Berlin: ' + str(count_non_berlin))

if __name__ == "__main__":
	audit_postcode_berlin()


##########################################################################
##########################################################################

# Auditing streets

def audit_streets():

	"""
	Checks whether any street names are abbreviated by ending in '.'
	(e.g. Friedrichstr. instead of Friedrichstraße).
	"""

	for _, elem in ET.iterparse(osm_file):

		abbreviated_streets = set()

		for tag in elem.iter():
			try:
				if tag.attrib["k"] == "addr:street":
					if tag.attrib["v"].strip()[-1] == '.':
						abbreviated_streets.add(tag.attrib["v"])
					else:
						continue
			except:
				continue
	pprint.pprint(abbreviated_streets)

if __name__ == "__main__":
	audit_streets()
# Returns an empty set.

##########################################################################

def audit_street_spelling():

	"""
	Tests whether alternative spelling "Strasse" exists 
	inplace of German "Straße".
	"""

	for _, elem in ET.iterparse(osm_file):

		alternative_spelling = set()

		for tag in elem.iter():
			try:
				if tag.attrib["k"] == "addr:street":
					
					if re.search('strasse', tag.attrib["v"], re.IGNORECASE):
						alternative_spelling.add(tag.attrib["v"])
					else:
						continue
			except:
				continue
	pprint.pprint(alternative_spelling)

if __name__ == "__main__":
	audit_street_spelling()

# Only returns: {'Peter-Strasser-Weg'}
# 0 problems, street is consistently spelled "Straße" and not abbreviated
