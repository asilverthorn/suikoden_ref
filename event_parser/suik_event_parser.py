import json
import sys, io
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
	def __init__(self, index: int, event_dat_json: dict[str, Any], form_sp_param_tracker: SpecialParamsTracker, com_sp_param_tracker: SpecialParamsTracker):
		self.index = index
		self.etyp = event_dat_json["etyp"]

		try:
			self.event_form = EventForm(event_dat_json["eventForm"], form_sp_param_tracker)
			self.event_com = EventCom(event_dat_json["eventCom"], com_sp_param_tracker)
		except ValueError as e:
			raise ValueError(f"{e} @ eventdat: {self.event_dat_index}")

	def print_info(self, tabs: int):
		tab_print(tabs, f"eventdat {self.index}; etyp: {self.etyp}")
		self.event_form.print_info(tabs + 1)
		self.event_com.print_info(tabs + 1)

class EventObj:
	"""
	Holds an individual eventobj from a Map JSON file
	"""
	def __init__(self, index: int, event_obj_json: dict[str, int]):
		self.index = index
		# read in all of the attributes from the JSON
		for key, value in event_obj_json.items():
			setattr(self, key, value)

class MapEventDat:
	"""
	Holds an individual mapeventdat and map from a Map JSON file
	"""

	def __init__(self, index: int, map_event_json: dict[str, Any], map_json: dict[str, Any] | None, form_sp_param_tracker: SpecialParamsTracker, com_sp_param_tracker: SpecialParamsTracker):
		self.index = index
		self.event_dat = []
		self.event_obj = []
		for index, event_dat_json in enumerate(map_event_json["eventdat"]):
			try:
				self.event_dat.append(EventDat(index, event_dat_json, form_sp_param_tracker, com_sp_param_tracker))
			except ValueError as e:
				raise ValueError(f"{e} @ mapeventdat: {self.index}")
			
		for index, event_obj_json in enumerate(map_event_json["eventobj"]):
			self.event_obj.append(EventObj(index, event_obj_json))
		
		self.map_json = map_json

	def print_info(self, tabs):
		tab_print(tabs, f"mapeventdat {self.index}")
		for event in self.event_dat:
			event.print_info(tabs+1)

	def plot(self, map_name: str):
		# Plot setup
		fig, ax = plt.subplots(figsize=(8, 8))

		# Draw each event_obj
		for i, item in enumerate(self.event_obj):
			x = item.x# * 8 # *8 is a guess
			y = item.y# * 8 # *8 is a guess
			w = item.w# * 8
			h = item.h# * 8
			
			if x > 0 and y > 0:
				# 0, 0 seems to be a placeholder location
				if w > 0 and h > 0:
					# Draw a rectangle if width/height are present
					rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='red', facecolor='none')
					ax.add_patch(rect)
					label_x = x + w / 2
					label_y = y + h / 2
				else:
					# Draw a point otherwise
					ax.plot(x, y, 'r.')
					label_x = x + 0.1
					label_y = y + 0.1

				ax.text(label_x, label_y, f"{i}", fontsize=8)

		# # Draw each tokushy_atari
		# for i, item in enumerate(self.map_json["tokusyu_atari"]):
		# 	x = item["x"]
		# 	y = item["y"]
		# 	w = item["w"]
		# 	h = item["h"]
		# 	if w > 0 and h > 0:
		# 		# Draw a rectangle if width/height are present
		# 		rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='green', facecolor='none')
		# 		ax.add_patch(rect)
		# 		label_x = x + w / 2
		# 		label_y = y + h / 2
		# 	else:
		# 		# Draw a point otherwise
		# 		ax.plot(x, y, 'g.')
		# 		label_x = x + 0.1
		# 		label_y = y + 0.1

		# 	ax.text(label_x, label_y, f"{i}", fontsize=8)

		# Final plot settings
		ax.set_title(f"Map of Obj locations for {map_name} - {self.index}")
		ax.set_xlabel("X")
		# ax.set_xlim(0, self.map_json["maxw"])
		# ax.set_ylim(0, self.map_json["maxh"])
		ax.set_ylabel("Y")
		ax.grid(True)
		ax.set_aspect('equal', 'box')
		plt.gca().invert_yaxis()
		plt.show()

class MapMonoBehavior:
	"""
	Holds the overall MonoBehavior from a map JSON file
	"""
	def __init__(self, map_file_json: dict[str, Any], text_map: dict[int, str] | None, text_tbl: dict[int, int] | None = None):
		# gather the MapEventData
		map_event_dat_json = map_file_json["eventdata"]["mapeventdat"]
		map_json = map_file_json["map"]
		sce_msg = map_file_json["eventdata"]["sce_msg"]
		m_name = map_file_json["m_Name"]
		self.form_sp_param_tracker = SpecialParamsTracker(sce_msg, m_name)
		self.com_sp_param_tracker = SpecialParamsTracker(sce_msg, m_name, text_tbl, map_file_json["overlay_func"])
		self.map_event_dat = []
		for map_event_index, map_event_json in enumerate(map_event_dat_json):
			map_no = map_event_json["mapno"]
			specific_map_json = None
			if map_no in map_json:
				# this is not the case with 3 map files: vc12, vj21, and vj23; in those, mapno seems to start at 1, whereas elsewhere it starts at 0
				specific_map_json = map_json[map_no]
			self.map_event_dat.append(MapEventDat(map_event_index, map_event_json, specific_map_json, self.form_sp_param_tracker, self.com_sp_param_tracker))
		
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

	def plot(self):
		for map_event in self.map_event_dat:
			map_event.plot(self.name)

def parse_arguments() -> Namespace:
	"""
	Parse command line arguments and returns the resulting args
	"""
	parser = ArgumentParser()
	parser.add_argument("-i", dest = "input_file", required = True, help = "JSON file exported from AssetStudio")
	parser.add_argument("-t", dest = "text_file", required = False, help = "text_gsd2 file for translating text strings")
	parser.add_argument("-tt", dest = "text_tbl", required = False, help = "text_gsd2_tbl file used to lookup reused text ids")
	parser.add_argument("-p", dest = "plot_maps", action = "store_true", required = False, help = "if set, also generates a matplotlib of event_objs")
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

	text_tbl = None
	if args.text_tbl:
		text_tbl_json = open_json_file(args.text_tbl)
		text_tbl = {item["srcId"]: item["dstId"] for item in text_tbl_json["tableList"]}

	mmb = MapMonoBehavior(map_file_json, text_map, text_tbl)
	mmb.print_info()
	if args.plot_maps:
		mmb.plot()