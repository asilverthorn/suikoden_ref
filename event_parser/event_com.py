from typing import List, Any
from event_commands.event_com_commands import EventComCommands
from event_commands.event_command import parse_event_cmds
from special_params import SpecialParamsTracker
from utils import tab_print



class EventCom:
	"""
	Holds an individual eventCom, which represents the event commands to be run
	"""
	def __init__(self, event_com_json: dict[str, Any], sp_param_tracker: SpecialParamsTracker):
		self.com_json = event_com_json
		self.sp_param_tracker = sp_param_tracker
		self.parsed_coms = parse_event_cmds(event_com_json, sp_param_tracker, EventComCommands)

	def __parse(self):
		self.parsed_coms = []
		i = 0

		# Read each command in and construct self.parsed_coms

	def print_info(self, tabs: int):
		tab_print(tabs, "eventcom:")
		for parsed_com in self.parsed_coms:
			parsed_com.print_info(tabs+1)
