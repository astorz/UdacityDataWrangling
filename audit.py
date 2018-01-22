import xml.etree.cElementTree as ET
import pprint
import re

osm_file = '../data/raw-data/berlin_medium.osm'

def audit_phone():

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

# def audit_shop():

# 	shops = {}

# 	for _, elem in ET.iterparse(osm_file):

# 		for tag in elem.iter():
# 			try:
# 				items = tag.items()
# 				if items[0][0] == 'k' and items[0][1] == 'amenity':

# 					shop = items[1][1]

# 					if shop not in shops:
# 						shops[shop] = 1
# 					else:
# 						shops[shop] += 1
# 			except:
# 				continue

# 	pprint.pprint(shops)
# if __name__ == "__main__":
# 	audit_shop()

ignore = ['vacant', 'yes']

mapping = {'alcohol': 'liquor_store',
 'antiques': 'antique_shop',
 'art': 'art_shop',
 'bag': 'bag_store',
 'beauty': 'beauty_shop',
 'bed': 'bedroom_store',
 'beverages': 'beverages_shop',
 'bicycle': 'bicycle_shop',
 'books': 'book_store',
 'car': 'car_dealership',
 'carpet': 'carpet_store',
 'clothes': 'cloting_store',
 'coffee': 'coffee_shop',
 'computer': 'computer_shop',
 'confectionery': 'pastry_shop',
 'convenience': 'convenience_store',
 'curtain': 'curtain_shop',
 'doityourself': 'diy_store',
 'dry_cleaning': 'dry_cleaner',
 'e-cigarette': 'e-cigarette_shop',
 'electric': 'electrical_supply_store',
 'electronics': 'electronics_store',
 'equestrian': 'saddlery',
 'erotic': 'erotic_store',
 'fabric': 'fabric_shop',
 'fashion': 'cloting_store',
 'furniture': 'furniture_store',
 'gemstones': 'gemstones_shop',
 'gift': 'gift_shop',
 'hardware': 'hardware_store',
 'ice_cream': 'ice_cream_shop',
 'jewelry': 'jeweler',
 'massage': 'massage_studio',
 'mobile_phone': 'mobile_phone_shop',
 'music': 'music_shop',
 'nails': 'nail_salon',
 'outdoor': 'outdoor_shop',
 'paint': 'paint_shop',
 'pet': 'pet_shop',
 'photo': 'photo_shop',
 'second_hand': 'second_hand_shop',
 'sewing': 'tailor',
 'shoes': 'shoe_shop',
 'sports': 'sports_shop',
 'stationery': 'stationery_shop',
 'tattoo': 'tattoo_parlor',
 'tea': 'tea_shop',
 'ticket': 'ticket_shop',
 'tobacco': 'tobacco_shop',
 'toys': 'toy_shop',
 'tyres': 'tire_shop',
 'wine': 'wine_shop',
 'woodcraft': 'woodcraft_shop'}


# Amenities
amenities = {'animal_boarding': 3,
 'animal_shelter': 6,
 'arts_centre': 42,
 'atm': 123,
 'baby_hatch': 3,
 'bank': 93,
 'bar': 108,
 'bbq': 6,
 'bench': 1719,
 'bench;shelter': 3,
 'bicycle_parking': 501,
 'bicycle_rental': 30,
 'biergarten': 51,
 'boat_rental': 15,
 'boathouse': 3,
 'brothel': 21,
 'bureau_de_change': 6,
 'cafe': 417,
 'canteen': 3,
 'car_rental': 15,
 'car_sharing': 3,
 'car_wash': 57,
 'casino': 9,
 'charging_station': 24,
 'childcare': 18,
 'cinema': 15,
 'clinic': 12,
 'clock': 45,
 'college': 15,
 'community_centre': 42,
 'compressed_air': 6,
 'courthouse': 15,
 'coworking_space': 3,
 'dancing_school': 3,
 'dentist': 78,
 'doctors': 123,
 'drinking_water': 15,
 'driving_school': 21,
 'embassy': 27,
 'emergency_service': 12,
 'fast_food': 357,
 'ferry_terminal': 9,
 'fire_station': 132,
 'fountain': 90,
 'fuel': 156,
 'gallery': 3,
 'grave_yard': 81,
 'grit_bin': 27,
 'health_centre': 3,
 'healthcare': 3,
 'hospital': 21,
 'hunting_stand': 438,
 'ice_cream': 18,
 'internet_cafe': 3,
 'kindergarten': 432,
 'library': 39,
 'lockers': 3,
 'marketplace': 21,
 'motorcycle_parking': 6,
 'nightclub': 24,
 'nursing_home': 18,
 'office': 3,
 'parking': 2310,
 'parking_entrance': 33,
 'parking_space': 102,
 'pharmacy': 198,
 'place_of_worship': 330,
 'police': 36,
 'post_box': 555,
 'post_office': 63,
 'prison': 3,
 'pub': 186,
 'public_bookcase': 3,
 'public_building': 27,
 'recycling': 570,
 'research_institute': 3,
 'restaurant': 927,
 'retirement_home': 6,
 'sauna': 6,
 'school': 279,
 'shelter': 198,
 'shower': 9,
 'social_centre': 3,
 'social_facility': 87,
 'sports_club': 3,
 'stables': 3,
 'stripclub': 3,
 'studio': 12,
 'swimming_pool': 3,
 'swingerclub': 3,
 'taxi': 75,
 'telephone': 210,
 'theatre': 45,
 'ticket_validator': 3,
 'toilets': 144,
 'townhall': 18,
 'toys_rental': 3,
 'university': 27,
 'unknown': 3,
 'vehicle_inspection': 6,
 'vending_machine': 228,
 'veterinary': 36,
 'waste_basket': 546,
 'waste_disposal': 9,
 'water': 3,
 'watering_place': 6}


## Auditing zip codes

# def audit_postcode():

# 	unique_postcodes = set()

# 	regex_postcode = r'^\d{5}$'

# 	for _, elem in ET.iterparse(osm_file):

# 		for tag in elem.iter():
# 			try:
# 				if tag.attrib["k"] == "addr:postcode":
# 					m = re.match(regex_postcode, tag.attrib["v"])
# 					if not m:
# 						unique_postcodes.add(tag.attrib["v"])
# 			except:
# 				continue

# 	pprint.pprint(sorted(unique_postcodes))

# if __name__ == "__main__":
# 	audit_postcode()

# def audit_postcode_berlin():

# 	"""Tests whether a postcode is in Berlin.
# 	Valid postcodes range from 10115-14199 
# 	(http://www.postleitzahlen-berlin.com/).
# 	"""

# 	count_berlin = 0
# 	count_non_berlin = 0
# 	non_berlin = set()

# 	for _, elem in ET.iterparse(osm_file):

# 		for tag in elem.iter():
# 			try:
# 				if tag.attrib["k"] == "addr:postcode":
# 					if not 10115 <= int(tag.attrib["v"]) <= 14199:
# 						count_non_berlin += 1
# 						non_berlin.add(tag.attrib["v"])
# 					else:
# 						count_berlin += 1
# 			except:
# 				continue
	
# 	pprint.pprint(non_berlin)
# 	print('Count Berlin: ' + str(count_berlin))
# 	print('Count Non-Berlin: ' + str(count_non_berlin))

# if __name__ == "__main__":
# 	audit_postcode_berlin()


# def audit_streets():

# 	"""
# 	Checks whether any street names are abbreviated by ending in '.'
# 	(e.g. Friedrichstr. instead of Friedrichstraße).
# 	"""

# 	for _, elem in ET.iterparse(osm_file):

# 		abbreviated_streets = set()

# 		for tag in elem.iter():
# 			try:
# 				if tag.attrib["k"] == "addr:street":
# 					if tag.attrib["v"].strip()[-1] == '.':
# 						abbreviated_streets.add(tag.attrib["v"])
# 					else:
# 						continue
# 			except:
# 				continue
# 	pprint.pprint(abbreviated_streets)

# if __name__ == "__main__":
# 	audit_streets()
# # Returns an empty set.


# def audit_street_spelling():

# 	"""
# 	Tests whether alternative spelling "Strasse" exists 
# 	inplace of German "Straße".
# 	"""

# 	for _, elem in ET.iterparse(osm_file):

# 		alternative_spelling = set()

# 		for tag in elem.iter():
# 			try:
# 				if tag.attrib["k"] == "addr:street":
					
# 					if re.search('strasse', tag.attrib["v"], re.IGNORECASE):
# 						alternative_spelling.add(tag.attrib["v"])
# 					else:
# 						continue
# 			except:
# 				continue
# 	pprint.pprint(alternative_spelling)

# if __name__ == "__main__":
# 	audit_street_spelling()

# # Only returns: {'Peter-Strasser-Weg'}
# # 0 problems, street is consistently spelled "Straße" and not abbreviated
