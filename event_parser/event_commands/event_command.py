from typing import List, Any, Callable
from special_params import *

class EventCommand:
	"""
	Holds the config for an individual Event Command (whether it be eventform or eventcom)
	num_params = -1 if it's variable length
	"""
	def __init__(self, num_params: int, short_name: str, special_params: dict = {}, desc: str = "", variable_len_func: Callable[[List[int], int], List[int]] | None = None):
		self.num_params = num_params
		self.short_name = short_name
		self.special_params = special_params
		self.desc = desc
		self.variable_len_func = variable_len_func

class ParsedEventCommand:
	"""
	Holds an individual eventform or eventcom command and parameters
	"""
	def __init__(self, cmd_id: int, params: List[int], sp_param_tracker: SpecialParamsTracker, event_cmd_map: dict[int, EventCommand], variable_len: bool = False):
		self.cmd_id = cmd_id
		self.params = params
		self.sp_param_tracker = sp_param_tracker
		self.parsed_params = ""
		self.event_cmd_map = event_cmd_map
		if variable_len:
			self.parsed_params = f"(variable params... {params})"
		else:
			i = 0
			while i < len(self.params):
				(parsed_param, i_skip) = self.get_parsed_param(i, self.params[i], params)
				self.parsed_params += parsed_param
				i += (1 + i_skip)

	def get_parsed_param(self, param_idx: int, param: int, all_params: List[int]) -> (str, int):
		"""
		Parse the parameter into a string
		If it's a special parameter, also read the other bytes specified and get the string for it.

		Returns a tuple containing the string and the number of bytes to skip ahead in the params List
		"""
		event_form_cmd = self.event_cmd_map[self.cmd_id]
		default = f"{param} "
		if(param_idx in event_form_cmd.special_params):
			# it has a special parameter, use its value
			special_param = event_form_cmd.special_params[param_idx]
			special_param_str = special_param[0]
			num_other_bytes = special_param[1]
			
			# Form the tuple out of all of the other bytes specified
			special_param_bytes = [param]
			for i in range(num_other_bytes):
				special_param_bytes.append(all_params[param_idx + i + 1])
			param = tuple(special_param_bytes)
				
			self.sp_param_tracker.add(special_param_str, param)
			return (get_special_param_str(special_param[0], param), num_other_bytes)
		else:
			return (default, 0)

	def print_info(self, tabs: int):
		event_form_cmd = self.event_cmd_map[self.cmd_id]
		short_name = event_form_cmd.short_name

		if 'NOP' != short_name and 'END' != short_name: # ignore END and NOP
			tab_print(tabs, f"{short_name}({self.cmd_id}) {self.parsed_params}")

def parse_event_cmds(event_json: List[int], sp_param_tracker: SpecialParamsTracker, event_cmd_map: dict[int, EventCommand]) -> List[ParsedEventCommand]:
		"""
		Parse the commands out of the given JSON based on the num_params specified in the given event_cmd_map
		Updates sp_param_tracker with any "special params" encounted
		"""
		parsed_cmds = []
		i = 0

		# Read each command in and construct self.parsed_forms based on the number of parameters
		while(i < len(event_json)):
			# Read the cmd_id
			cmd_id = event_json[i]
			i+=1

			# Validate that cmd_id is valid
			if cmd_id not in event_cmd_map:
				# we're about to die -- print out the parsed commands up to this point
				for parsed_cmd in parsed_cmds:
					parsed_cmd.print_info(0)

				raise ValueError(f"{cmd_id} not found in event_cmd_map")

			# Read the parameters
			num_params = event_cmd_map[cmd_id].num_params
			# Validate that the num_params doesn't put us beyond the end of the eventform/eventcom
			if i + num_params > len(event_json):
				# we're about to die -- print out the parsed command up to this point
				for parsed_cmd in parsed_cmds:
					parsed_cmd.print_info(0)

				raise ValueError(f"invalid number of parameters: {num_params} at index {i} for cmd_id {cmd_id}")
			
			params = []
			variable_len = (-1 == num_params)
			if variable_len:
				if event_cmd_map[cmd_id].variable_len_func: # there's a function that tells us how long it is
					try:
						params = event_cmd_map[cmd_id].variable_len_func(event_json, i)
						variable_len = False # marking false so that it gets printed out and the loop continues
						num_params = len(params)
					except ValueError as e:
						# we're about to die -- print out the parsed command up to this point
						for parsed_cmd in parsed_cmds:
							parsed_cmd.print_info(0)
						raise ValueError(f"Failed to execute variable length function for cmd_id {cmd_id} {e}")
				else: # no function. We're going to just read in the rest of the commands to dump it to the output file
					params = event_json[i:]
			else: # Fixed number of params
				if 0 < num_params:
					params = event_json[i:i+num_params]

			parsed_cmds.append(ParsedEventCommand(cmd_id, params, sp_param_tracker, event_cmd_map, variable_len))

			# go to next
			if not variable_len:
				i+=num_params
			else:
				# it's variable length; exit out of the loop, because we can't parse any farther
				i = len(event_json)
		
		return parsed_cmds