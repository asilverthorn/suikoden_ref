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

	def print_info(self, tabs: int):
		tab_print(tabs, "eventcom:")
		for parsed_com in self.parsed_coms:
			parsed_com.print_info(tabs+1)


# convenience mechanism to parse a string of ints
import sys
if __name__ == '__main__':
	arg = sys.argv[1]
	try:
		int_list = list(map(int, arg.split(",")))
	except ValueError:
		int_list = list(map(int, arg.split(" ")))

	sp_param_tracker = SpecialParamsTracker()
	EventCom(int_list, sp_param_tracker).print_info(0)