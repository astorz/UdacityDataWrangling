"""
This script contains all the helper functions used to update the xml data
before it is written out to .json as part of the programmatic cleaning step.
"""

import xml.etree.cElementTree as ET
import pprint
import re

def update_phone(phone):
	orig = phone

	# Splitting string into multiple phone numbers on either ";" or ","
	phone = [x.strip() for x in re.split(";|,", phone)]

	# Remove second "+", i.e. "++" --> "+"
	phone = [p.replace("++", "+") for p in phone]

	# Removing all non-numerical characters except "+"
	not_remove = "+"
	regex = r'[^\d'+not_remove+']'
	phone = [re.sub(regex, '', x) for x in phone]

	# Splitting phone numbers if a second number beginning with +49 occurs in string
	for p in phone:
		if "+49" in p[1:]:
			phone = ["+" + x.strip() for x in p[1:].split("+")]

	# Changing "0049" into "+49"
	phone = [x.replace("0049", "+49") if x[:4] == "0049" else x for x in phone]

	# Adding "+" if phone number starts with "49"
	regex_49 = r'^49'
	phone = [re.sub(regex_49, '+49', x) for x in phone]

	# Adding international country code "+49" if phone number starts with "0" (i.e., a landline with area code or a mobile number)
	phone = [''.join(['+49', x[1:]]) if x[0] == "0" else x for x in phone]

	# Testing phone number (must now start with "+49"; otherwise original value is retained):
	if phone_validate(phone):
		return orig
	
	return '; '.join(phone)

def phone_validate(phone):
	reg = r'^\+49\d+$'
	for p in phone:
		m = re.search(reg, p)
		if not m:
			return "problem"
		else:
			return None

### Cleaning and changing 'shops' into 'amenities'

IGNORE = ['vacant', 'yes']

MAPPING = {'alcohol': 'liquor_store',
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


def update_shop(node):
	
	if node["shop"] in IGNORE:
		node.pop("shop")
	elif node["shop"] in MAPPING:
		node["amenity"] = MAPPING[node.pop("shop")]
	else:
		node["amenity"] = node.pop("shop")
		# See: https://stackoverflow.com/questions/16475384/rename-a-dictionary-key
	
	return node


