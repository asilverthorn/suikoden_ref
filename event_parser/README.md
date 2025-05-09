
This tool is used to parse the eventForm and eventCom from Suikoden II Monobehavior json files exported by AssetStudio.

### Exporting from AssetStudio.GUI
AssetStudio fork link: https://github.com/aelurum/AssetStudio

To export map JSON files from AssetStudio.GUI:

1) Options -> Specify Unity Version. Type in "2022.3.28f1" (no quotes)
2) File -> Load Folder. Select <Steam Library>\steamapps\Common\Suikoden I and II HD Remaster\Suikoden I and II HD Remaster_Data\StreamingAssets\aa\StandaloneWindows64
3) Wait a few minutes. You should see it Loading .bundle files in its Debug Console
4) Filter Type -> TextAsset. In the Asset List search bar, search for "text_gsd2_en". Right click and "Export selected asset".
5) Filter Type -> MonoBehavior. Search for assets that start with `v` and are 4 characters. Example: va01. Right click and export the ones that you're interested in.

The second character in the asset name refers to the major world map area. They are:

- a = Kyaro area
- b = Mercenary Fort area
- c = Muse area
- d = Radat / South Window area
- e = Greenhill area
- f = Gregminster area
- g = Tinto area
- h = Two Rivers area
- i = Rockaxe area
- j = L'Ren area
- k = HQ 

### Running the tool

`py suik_event_parser.py -i MonoBehaviour/vf02.json -t TextAsset/text_gsd2_en`

(the `-t` parameter is optional -- if not available, it will not attempt to lookup the name of the map file)

### Example output

At the top of the output, the script will print out any "Special Params" identified -- these are an attempt to locate patterns in the parameters across events, such as character names, AREA_NOs, and EVENT_FLAGs.

```
	Map: Gregminster(455)
	Form Special Params used: 
		EVENT_FLAG: 50 62 64 65 68 150 151 
		CHANO: Lorelai(14) Killey(44) McDohl(82) Gremio(125) 172 
	Com Special Params used:
		WINDOW_MFNO: 0 1 2 3 4 
		AREA_NO: Gregminster_Area_F(5) 13 
		FILE_NO: 2 3 28 
		CHANO: Lorelai(14) Killey(44) McDohl(82) Gremio(125) 172 
	eventdata:
		mapeventdat 0
			eventdat 0; etyp: 1
				eventform:
					EVENT_HUMAN(5) 25 
				eventcom:
					WindowHenji(23) 2 0 
			eventdat 1; etyp: 1
				eventform:
					EVENT_HUMAN(5) 26 
				eventcom:
					WindowHenji(23) 2 1 
			eventdat 2; etyp: 1
				eventform:
					EVENT_HUMAN(5) 27 
				eventcom:
					WindowHenji(23) 2 2 
			eventdat 3; etyp: 1
				eventform:
					EVENT_HUMAN(5) 28 
				eventcom:
					WindowHenji(23) 2 3 
			eventdat 4; etyp: 1
				eventform:
					EVENT_HUMAN(5) 29 
				eventcom:
					WindowHenji(23) 2 4 
			eventdat 5; etyp: 1
				eventform:
					EVENT_HUMAN(5) 30 
				eventcom:
					WindowHenji(23) 2 5 
					ODirSet(3) 30 0 
			eventdat 6; etyp: 1
				eventform:
					EVENT_HUMAN(5) 31 
				eventcom:
					WindowHenji(23) 2 6 
			eventdat 7; etyp: 1
				eventform:
					EVENT_HUMAN(5) 32 
				eventcom:
					WindowHenji(23) 2 7 
			eventdat 8; etyp: 1
				eventform:
					EVENT_HUMAN(5) 33 
				eventcom:
					WindowHenji(23) 2 8 
			eventdat 9; etyp: 1
				eventform:
					EVENT_HUMAN(5) 34 
					event_flag_AND(4) 50 2 
					potch(18) 1 7 
				eventcom:
					WindowHenji(23) 2 9 
					TimWait(73) 20 
					WindowSentaku(40) (variable params... )
			....
```

### Misc Notes
- At present, some of the eventComs have a variable number of parameters for which the logic hasn't been reverse engineered. As a result, this parser will get to those and stop parsing the rest of the eventCom.

- For descriptions of the commands, please see event_commands/event_com_commands.py and event_commands/event_form_commands.py.

- If you want to parse everything, I recommend downloading git bash and running a command like the following from your exports MonoBehavior directory: `for file in v[a-z][0-9][0-9].json; do echo "Processing $file" >&2; py ../suik_event_parser.py -i $file -t ../TextAsset/text_gsd2_en; done > parsed_events.txt 2>&1`