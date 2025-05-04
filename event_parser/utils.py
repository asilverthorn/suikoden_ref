def tab_print(tabs: int, str: str):
	# avoid issues with unprintable characters by encoding and reencoding as utf-8
	output_str = str.encode("utf-8", errors="replace").decode("utf-8")
	print('\t' * tabs + output_str)