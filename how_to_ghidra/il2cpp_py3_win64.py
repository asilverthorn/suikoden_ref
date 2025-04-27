#@runtime PyGhidra
# Generated script file by Il2CppInspectorRedux - https://github.com/LukeFZ (Original Il2CppInspector by http://www.djkaty.com - https://github.com/djkaty)
# Target Unity version: 2021.3.0 - 2023.1.99

import json
import os
from datetime import datetime
import abc

class BaseStatusHandler(abc.ABC):
	def initialize(self): pass
	def shutdown(self): pass

	def update_step(self, name: str, max_items: int = 0): print(f"{name} {max_items}")
	def update_progress(self, progress: int = 1): pass

	def was_cancelled(self): return False

class BaseDisassemblerInterface(abc.ABC):
	supports_fake_string_segment: bool = False

	@abc.abstractmethod
	def get_script_directory(self) -> str: return ""

	@abc.abstractmethod
	def on_start(self): pass

	@abc.abstractmethod
	def on_finish(self): pass

	@abc.abstractmethod
	def define_function(self, address: int, end: int | None = None): pass

	@abc.abstractmethod
	def define_data_array(self, address: int, type: str, count: int): pass

	@abc.abstractmethod
	def set_data_type(self, address: int, type: str): pass

	@abc.abstractmethod
	def set_function_type(self, address: int, type: str): pass

	@abc.abstractmethod
	def set_data_comment(self, address: int, cmt: str): pass

	@abc.abstractmethod
	def set_function_comment(self, address: int, cmt: str): pass

	@abc.abstractmethod
	def set_data_name(self, address: int, name: str): pass

	@abc.abstractmethod
	def set_function_name(self, address: int, name: str): pass

	@abc.abstractmethod
	def add_cross_reference(self, from_address: int, to_address: int): pass

	@abc.abstractmethod
	def import_c_typedef(self, type_def: str): pass

	# optional
	def add_function_to_group(self, address: int, group: str): pass
	def cache_function_types(self, function_types: list[str]): pass

	# only required if supports_fake_string_segment == True
	def create_fake_segment(self, name: str, size: int) -> int: return 0

	def write_string(self, address: int, value: str) -> int: pass
	def write_address(self, address: int, value: int): pass

class ScriptContext:
	_backend: BaseDisassemblerInterface
	_status: BaseStatusHandler

	def __init__(self, backend: BaseDisassemblerInterface, status: BaseStatusHandler) -> None:
		self._backend = backend
		self._status = status

	def from_hex(self, addr: str): 
		return int(addr, 0)

	def parse_address(self, d: dict): 
		return self.from_hex(d['virtualAddress'])

	def define_il_method(self, definition: dict):
		addr = self.parse_address(definition)
		self._backend.set_function_name(addr, definition['name'])
		self._backend.set_function_type(addr, definition['signature'])
		self._backend.set_function_comment(addr, definition['dotNetSignature'])
		self._backend.add_function_to_group(addr, definition['group'])

	def define_il_method_info(self, definition: dict):
		addr = self.parse_address(definition)
		self._backend.set_data_type(addr, r'struct MethodInfo *')
		self._backend.set_data_name(addr, definition['name'])
		self._backend.set_data_comment(addr, definition['dotNetSignature'])
		if 'methodAddress' in definition:
			method_addr = self.from_hex(definition["methodAddress"])
			self._backend.add_cross_reference(method_addr, addr)
			
	def define_cpp_function(self, definition: dict):
		addr = self.parse_address(definition)
		self._backend.set_function_name(addr, definition['name'])
		self._backend.set_function_type(addr, definition['signature'])

	def define_string(self, definition: dict):
		addr = self.parse_address(definition)
		self._backend.set_data_type(addr, r'struct String *')
		self._backend.set_data_name(addr, definition['name'])
		self._backend.set_data_comment(addr, definition['string'])

	def define_field(self, addr: str, name: str, type: str, il_type: str | None = None):
		address = self.from_hex(addr)
		self._backend.set_data_type(address, type)
		self._backend.set_data_name(address, name)
		if il_type is not None:
			self._backend.set_data_comment(address, il_type)

	def define_field_from_json(self, definition: dict):
		self.define_field(definition['virtualAddress'], definition['name'], definition['type'], definition['dotNetType'])

	def define_array(self, definition: dict):
		addr = self.parse_address(definition)
		self._backend.define_data_array(addr, definition['type'], int(definition['count']))
		self._backend.set_data_name(addr, definition['name'])

	def define_field_with_value(self, definition: dict):
		addr = self.parse_address(definition)
		self._backend.set_data_name(addr, definition['name'])
		self._backend.set_data_comment(addr, definition['value'])

	def process_metadata(self, metadata: dict):
		# Function boundaries
		function_addresses = metadata['functionAddresses']
		function_addresses.sort()
		count = len(function_addresses)

		self._status.update_step('Processing function boundaries', count)
		for i in range(count):
			start = self.from_hex(function_addresses[i])
			if start == 0:
				self._status.update_progress()
				continue

			end = self.from_hex(function_addresses[i + 1]) if i + 1 != count else None

			self._backend.define_function(start, end)
			self._status.update_progress()

		# Method definitions
		self._status.update_step('Processing method definitions', len(metadata['methodDefinitions']))
		self._backend.cache_function_types([x["signature"] for x in metadata['methodDefinitions']])
		for d in metadata['methodDefinitions']:
			self.define_il_method(d)
			self._status.update_progress()
		
		# Constructed generic methods
		self._status.update_step('Processing constructed generic methods', len(metadata['constructedGenericMethods']))
		self._backend.cache_function_types([x["signature"] for x in metadata['constructedGenericMethods']])
		for d in metadata['constructedGenericMethods']:
			self.define_il_method(d)
			self._status.update_progress()

		# Custom attributes generators
		self._status.update_step('Processing custom attributes generators', len(metadata['customAttributesGenerators']))
		self._backend.cache_function_types([x["signature"] for x in metadata['customAttributesGenerators']])
		for d in metadata['customAttributesGenerators']:
			self.define_cpp_function(d)
			self._status.update_progress()
		
		# Method.Invoke thunks
		self._status.update_step('Processing Method.Invoke thunks', len(metadata['methodInvokers']))
		self._backend.cache_function_types([x["signature"] for x in metadata['methodInvokers']])
		for d in metadata['methodInvokers']:
			self.define_cpp_function(d)
			self._status.update_progress()

		# String literals for version >= 19
		if 'virtualAddress' in metadata['stringLiterals'][0]:
			self._status.update_step('Processing string literals (V19+)', len(metadata['stringLiterals']))

			if self._backend.supports_fake_string_segment:
				total_string_length = 0
				for d in metadata['stringLiterals']:
					total_string_length += len(d["string"]) + 1
				
				aligned_length = total_string_length + (4096 - (total_string_length % 4096))
				segment_base = self._backend.create_fake_segment(".fake_strings", aligned_length)

				current_string_address = segment_base
				for d in metadata['stringLiterals']:
					self.define_string(d)

					ref_addr = self.parse_address(d)
					written_string_length = self._backend.write_string(current_string_address, d["string"])
					self._backend.set_data_type(ref_addr, r'const char* const')
					self._backend.write_address(ref_addr, current_string_address)

					current_string_address += written_string_length
					self._status.update_progress()
			else:
				for d in metadata['stringLiterals']:
					self.define_string(d)
					self._status.update_progress()

		# String literals for version < 19
		else:
			self._status.update_step('Processing string literals (pre-V19)')
			litDecl = 'enum StringLiteralIndex {\n'
			for d in metadata['stringLiterals']:
				litDecl += "  " + d['name'] + ",\n"
			litDecl += '};\n'

			self._backend.import_c_typedef(litDecl)
		
		# Il2CppClass (TypeInfo) pointers
		self._status.update_step('Processing Il2CppClass (TypeInfo) pointers', len(metadata['typeInfoPointers']))
		for d in metadata['typeInfoPointers']:
			self.define_field_from_json(d)
			self._status.update_progress()
		
		# Il2CppType (TypeRef) pointers
		self._status.update_step('Processing Il2CppType (TypeRef) pointers', len(metadata['typeRefPointers']))
		for d in metadata['typeRefPointers']:
			self.define_field(d['virtualAddress'], d['name'], r'struct Il2CppType *', d['dotNetType'])
			self._status.update_progress()
		
		# MethodInfo pointers
		self._status.update_step('Processing MethodInfo pointers', len(metadata['methodInfoPointers']))
		for d in metadata['methodInfoPointers']:
			self.define_il_method_info(d)
			self._status.update_progress()

		# FieldInfo pointers, add the contents as a comment
		self._status.update_step('Processing FieldInfo pointers', len(metadata['fields']))
		for d in metadata['fields']:
			self.define_field_with_value(d)
			self._status.update_progress()

		# FieldRva pointers, add the contents as a comment
		self._status.update_step('Processing FieldRva pointers', len(metadata['fieldRvas']))
		for d in metadata['fieldRvas']:
			self.define_field_with_value(d)
			self._status.update_progress()

		# IL2CPP type metadata
		self._status.update_step('Processing IL2CPP type metadata', len(metadata['typeMetadata']))
		for d in metadata['typeMetadata']:
			self.define_field(d['virtualAddress'], d['name'], d['type'])
		
		# IL2CPP function metadata
		self._status.update_step('Processing IL2CPP function metadata', len(metadata['functionMetadata']))
		for d in metadata['functionMetadata']:
			self.define_cpp_function(d)

		# IL2CPP array metadata
		self._status.update_step('Processing IL2CPP array metadata', len(metadata['arrayMetadata']))
		for d in metadata['arrayMetadata']:
			self.define_array(d)

		# IL2CPP API functions
		self._status.update_step('Processing IL2CPP API functions', len(metadata['apis']))
		self._backend.cache_function_types([x["signature"] for x in metadata['apis']])
		for d in metadata['apis']:
			self.define_cpp_function(d)

	def process(self):
		self._status.initialize()

		try:
			start_time = datetime.now()

			self._status.update_step("Running script prologue")
			self._backend.on_start()

			metadata_path = os.path.join(self._backend.get_script_directory(), "./metadata.json")
			with open(metadata_path, "r") as f:
				self._status.update_step("Loading JSON metadata")
				metadata = json.load(f)['addressMap']
				self.process_metadata(metadata)

			self._status.update_step("Running script epilogue")
			self._backend.on_finish()

			self._status.update_step('Script execution complete.')

			end_time = datetime.now()
			print(f"Took: {end_time - start_time}")

		except RuntimeError: 
			pass
		
		finally: 
			self._status.shutdown()
# Ghidra-specific implementation
from ghidra.app.cmd.function import ApplyFunctionSignatureCmd
from ghidra.app.util.cparser.C import CParserUtils
from ghidra.program.model.data import ArrayDataType
from ghidra.program.model.symbol import SourceType
from ghidra.program.model.symbol import RefType
from ghidra.app.cmd.label import DemanglerCmd
from ghidra.app.util.demangler import DemanglerOptions
from ghidra.app.util.demangler.gnu import GnuDemangler
from ghidra.app.services import DataTypeManagerService

#try:
#	from typing import TYPE_CHECKING
#	if TYPE_CHECKING:
#		from ..shared_base import BaseStatusHandler, BaseDisassemblerInterface, ScriptContext
#		import json
#		import os
#		import sys
#		from datetime import datetime
#except:
#	pass

class GhidraDisassemblerInterface(BaseDisassemblerInterface):
	supports_fake_string_segment = False

	def get_script_directory(self) -> str: 
		return getSourceFile().getParentFile().toString()

	def on_start(self):
		self.xrefs = currentProgram.getReferenceManager()

		print(f"Current program base address: {currentProgram.getImageBase()}")

		# Check that the user has parsed the C headers first
		if len(getDataTypes('Il2CppObject')) == 0:
			print('STOP! You must import the generated C header file (cpp\\appdata/il2cpp-types.h) before running this script.')
			print('See https://github.com/djkaty/Il2CppInspector/blob/master/README.md#adding-metadata-to-your-ghidra-workflow for instructions.')
			sys.exit()

		# Ghidra sets the image base for ELF to 0x100000 for some reason
		# https://github.com/NationalSecurityAgency/ghidra/issues/1020
		# Make sure that the base address is 0
		# Without this, Ghidra may not analyze the binary correctly and you will just waste your time
		# If 0 doesn't work for you, replace it with the base address from the output of the CLI or GUI
		if currentProgram.getExecutableFormat().endswith('(ELF)'):
			currentProgram.setImageBase(toAddr(0), True)
		
		# Don't trigger decompiler
		setAnalysisOption(currentProgram, "Call Convention ID", "false")

	def on_finish(self):
		pass

	def define_function(self, address: int, end: int | None = None):
		address_str = hex(address)
		address = toAddr(address_str)
		# Don't override existing functions
		fn = getFunctionAt(address)
		if fn is None:
			# Create new function if none exists
			try:
				createFunction(address, None)
			except Exception as e:
				print(f"Failed to create function at {address} -- {e}")

	def define_data_array(self, address: int, type: str, count: int):
		if type.startswith('struct '):
			type = type[7:]
		try:
			t = getDataTypes(type)[0]
			a = ArrayDataType(t, count, t.getLength())
			address_str = hex(address)
			address = toAddr(address_str)
			removeDataAt(address)
			createData(address, a)
		except Exception as e:
			print(f"Failed to set data array: {type} -- {e}")

	def set_data_type(self, address: int, type: str):
		if type.startswith('struct '):
			type = type[7:]
		
		try:
			t = getDataTypes(type)[0]
			address_str = hex(address)
			address = toAddr(address_str)

			removeDataAt(address)
			createData(address, t)
		except Exception as e:
			print(f"Failed to set type: {type} -- {e}")

	def set_function_type(self, address: int, type: str):
		typeSig = CParserUtils.parseSignature(DataTypeManagerService@None, currentProgram, type)
		address_str = hex(address)
		ApplyFunctionSignatureCmd(toAddr(address_str), typeSig, SourceType.USER_DEFINED, False, True).applyTo(currentProgram)

	def set_data_comment(self, address: int, cmt: str):
		address_str = hex(address)
		setEOLComment(toAddr(address_str), cmt)

	def set_function_comment(self, address: int, cmt: str):
		address_str = hex(address)
		setPlateComment(toAddr(address_str), cmt)

	def set_data_name(self, address: int, name: str):
		address_str = hex(address)
		address = toAddr(address_str)

		if len(name) > 2000:
			print("Name length exceeds 2000 characters, skipping (%s)" % name)
			return

		if not name.startswith("_ZN"):
			createLabel(address, name, True, SourceType.USER_DEFINED)
			return

		# Using the GnuDemangler directly rather than DemanglerCmd because the latter won't run 
		#  the GnuDemanglerbecause the executable type is a Windows PE. 
		#  GnuDemangler is what's needed for our _ZN mangled class names
		try:
			demanglerOptions = DemanglerOptions()
			demangler = GnuDemangler()
			demangled = demangler.demangle(name)
			
			if not demangled.applyTo(currentProgram, address, demanglerOptions, monitor):
				print(f"Failed to apply demangled name to {name} at {address}, falling back to mangled")
				createLabel(address, name, True, SourceType.USER_DEFINED)
		except Exception as e:
			print(f"Exception applying demangled name to {name} @{address} -- {e}")

	def set_function_name(self, address: int, name: str): 
		return self.set_data_name(address, name)

	def add_cross_reference(self, from_address: int, to_address: int): 
		from_address_str = hex(from_address)
		to_address_str = hex(to_address)
		self.xrefs.addMemoryReference(toAddr(from_address_str), toAddr(to_address_str), RefType.DATA, SourceType.USER_DEFINED, 0)

	def import_c_typedef(self, type_def: str):
		# Code declarations are not supported in Ghidra
		# This only affects string literals for metadata version < 19
		# TODO: Replace with creating a DataType for enums
		pass

class GhidraStatusHandler(BaseStatusHandler): 
	pass

status = GhidraStatusHandler()
backend = GhidraDisassemblerInterface()
context = ScriptContext(backend, status)
context.process()