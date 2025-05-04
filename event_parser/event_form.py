from typing import List, Any
from event_commands.event_form_commands import EventFormCommands
from event_commands.event_command import parse_event_cmds
from special_params import SpecialParamsTracker
from utils import tab_print

class EventForm:
	"""
	Holds an individual eventForm, which are the conditionals checked before the associated eventCom runs
	"""
	def __init__(self, event_form_json: List[int], sp_param_tracker: SpecialParamsTracker):
		self.form_json = event_form_json
		self.sp_param_tracker = sp_param_tracker

		self.parsed_forms = parse_event_cmds(event_form_json, sp_param_tracker, EventFormCommands)

	def print_info(self, tabs: int):
		tab_print(tabs, "eventform:")
		for parsed_form in self.parsed_forms:
			parsed_form.print_info(tabs+1)