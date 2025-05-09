import json
import sys, io

# Ensure that redirects get written with utf-8
if not sys.stdout.isatty():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from argparse import ArgumentParser, Namespace
from typing import Any

from event_form import EventForm
from event_com import EventCom
from special_params import SpecialParamsTracker
from utils import tab_print

class EventDat:
	"""
	Holds an individual eventdat from a Map JSON file, with 3 fields within it:
	 - etyp
	 - event_form
	 - event_com
	"""
	def __init__(self, event_dat_index: int, event_dat_json: dict[str, Any], form_sp_param_tracker: SpecialParamsTracker, com_sp_param_tracker: SpecialParamsTracker):
		self.event_dat_index = event_dat_index
		self.etyp = event_dat_json["etyp"]

		try:
			self.event_form = EventForm(event_dat_json["eventForm"], form_sp_param_tracker)
			self.event_com = EventCom(event_dat_json["eventCom"], com_sp_param_tracker)
		except ValueError as e:
			raise ValueError(f"{e} @ eventdat: {self.event_dat_index}")

	def print_info(self, tabs: int):
		tab_print(tabs, f"eventdat {self.event_dat_index}; etyp: {self.etyp}")
		self.event_form.print_info(tabs + 1)
		self.event_com.print_info(tabs + 1)

class MapEventDat:
	"""
	Holds an individual mapeventdat from a Map JSON file
	"""

	def __init__(self, map_event_index: int, map_event_json: dict[str, Any], form_sp_param_tracker: SpecialParamsTracker, com_sp_param_tracker: SpecialParamsTracker):
		self.map_event_index = map_event_index
		self.event_dat = []
		for event_dat_index, event_dat_json in enumerate(map_event_json["eventdat"]):
			try:
				self.event_dat.append(EventDat(event_dat_index, event_dat_json, form_sp_param_tracker, com_sp_param_tracker))
			except ValueError as e:
				raise ValueError(f"{e} @ mapeventdat: {self.map_event_index}")

	def print_info(self, tabs):
		tab_print(tabs, f"mapeventdat {self.map_event_index}")
		for event in self.event_dat:
			event.print_info(tabs+1)

class MapMonoBehavior:
	"""
	Holds the overall MonoBehavior from a map JSON file
	"""
	def __init__(self, map_file_json: dict[str, Any], text_map: dict[int, str] | None):
		# gather the MapEventData
		map_event_dat_json = map_file_json["eventdata"]["mapeventdat"]
		self.form_sp_param_tracker = SpecialParamsTracker()
		self.com_sp_param_tracker = SpecialParamsTracker()
		self.map_event_dat = []
		for map_event_index, map_event_json in enumerate(map_event_dat_json):
			self.map_event_dat.append(MapEventDat(map_event_index, map_event_json, self.form_sp_param_tracker, self.com_sp_param_tracker))
		
		# Get the name of this map from the text_map (if provided)
		name_idx = map_file_json["msdat"]["name"]
		self.name = f"{text_map.get(name_idx, name_idx)}({name_idx})" if text_map else f"{name_idx}"
	
	def print_info(self):
		tabs = 1
		tab_print(tabs, f"Map: {self.name}")
		tab_print(tabs, f"Form Special Params used: ")
		self.form_sp_param_tracker.print_info(tabs+1)
		tab_print(tabs, f"Com Special Params used:")
		self.com_sp_param_tracker.print_info(tabs+1)
		tab_print(tabs, f"eventdata:")
		for map_event in self.map_event_dat:
			map_event.print_info(tabs+1)

def parse_arguments() -> Namespace:
	"""
	Parse command line arguments and returns the resulting args
	"""
	parser = ArgumentParser()
	parser.add_argument("-i", dest = "input_file", required = True, help = "JSON file exported from AssetStudio")
	parser.add_argument("-t", dest = "text_file", required = False, help = "text_gsd2 file for translating text strings")
	return parser.parse_args()

def open_json_file(json_file_path: str) -> dict[str, Any]:
	""" 
	Opens the given JSON file and loads it
	"""
	with open(json_file_path, 'r', encoding='utf-8') as f:
		data = json.load(f)
		return data

if __name__ == '__main__':
	args = parse_arguments()
	map_file_json = open_json_file(args.input_file)

	# Read in the given text file, if any, and translate the "id"s into keys in a map
	text_map = None
	if args.text_file:
		text_file_json = open_json_file(args.text_file)
		text_map = {item["id"]: item["text"] for item in text_file_json["textList"]}

	mmb = MapMonoBehavior(map_file_json, text_map)
	mmb.print_info()