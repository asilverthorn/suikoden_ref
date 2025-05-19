
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
                EVENT_FLAG: (50, 2) (62, 8) (64, 16) (64, 32) (64, 64) (65, 4) (68, 1) S1SaveLoaded((150, 2)) (150, 4) (151, 64)
                CHANO: Lorelai(14) Killey(44) McDohl(82) Gremio(125) 172
                CHA_FLAG_MODE: 2
                MAP_IN_OUT_FLAG: (0, 1)
        Com Special Params used:
                WINDOW_MSG: 1006020012(0, 11) 1006020013(0, 12) 1006020014(0, 13) 1006020015(0, 14) 1006020016(0, 15) 1006020017(0, 16) 1006020018(0, 17) 1006020019(0, 18) 1006020060(1, 0) 1006020061(1, 1) 1006020062(1, 2) 1006020063(1, 3) 1006020064(1, 4) 1006020065(1, 5) 1006020066(1, 6) 1006020067(1, 7) 1006020068(1, 8) 1006020069(1, 9) 1006020070(1, 10) 1006020071(1, 11) 1006020072(1, 12) 1006020073(1, 13) 1006020074(1, 14) 1006020075(1, 15) 1006020076(1, 16) 1006020077(1, 17) 1006020078(1, 18) 1006020079(1, 19) 1006020080(1, 20) 1006020081(1, 21) 1006020082(1, 22) 1006020083(1, 23) 1006020084(1, 24) 1006020085(1, 25) 1006020101(2, 0) 1006020102(2, 1) 1006020103(2, 2) 1006020104(2, 3) 1006020105(2, 4) 1006020106(2, 5) 1006020107(2, 6) 1006020108(2, 7) 1006020109(2, 8) 1006020110(2, 9) 1006020111(2, 10) 1006020112(2, 11) 1006020113(2, 12) 1006020114(2, 13) 1006020115(2, 14) 1006020116(2, 15) 1006020117(2, 16) 1006020121(2, 20) 1006020201(3, 0) 1006020202(3, 1) 1006020203(3, 2) 1006020204(3, 3) 1006020205(3, 4) 1006020211(3, 10) 1006020212(3, 11) 1006020213(3, 12) 1006020214(3, 13) 1006020215(3, 14) 1006020216(3, 15) 1006020217(3, 16) 1006020218(3, 17) 1006020219(3, 18) 1006020220(3, 19) 1006020221(3, 20) 1006020222(3, 21) 1006020223(3, 22) 1006020224(3, 23) 1006020225(3, 24) 1006020226(3, 25) 1006020227(3, 26) 1006020228(3, 27) 1006020229(3, 28) 1006020230(3, 29) 1006020231(3, 30) 1006020232(3, 31) 1006020233(3, 32) 1006020234(3, 33) 1006020235(3, 34) 1006020236(3, 35) 1006020237(3, 36) 1006020238(3, 37) 1006020239(3, 38) 1006020240(3, 39) 1006020241(3, 40) 1006020242(3, 41) 1006020243(3, 42) 1006020244(3, 43) 1006020245(3, 44) 1006020246(3, 45) 1006020247(3, 46) 1006020248(3, 47) 1006020249(3, 48) 1006020250(3, 49) 1006020251(3, 50) 1006020252(3, 51) 1006020253(3, 52) 1006020254(3, 53) 1006020255(3, 54) 1006020256(3, 55) 1006020257(3, 56) 1006020258(4, 0) 1006020259(4, 1) 1006020260(4, 2) 1006020261(4, 3) 1006020262(4, 4)
                SOUND: (0, 193) (1, 0) (4, 6) (4, 7) (5, 0) (5, 176) (9, 7) (9, 8) (9, 9)
                EVENT_FLAG: (50, 2) (68, 1)
                AREA_NO: Gregminster_Area_F(5) 13
                FILE_NO: 2 3 28
                MAP_IN_OUT_FLAG: (0, 1)
                CHANO: Lorelai(14) Killey(44) McDohl(82) Gremio(125) 172
                CHA_FLAG_MODE: StartRecruit(30) Recruit(31)
        eventdata:
                mapeventdat 0
                        eventdat 0; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 25
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020101(2, 0)
                                        LABEL(255) 254
                        eventdat 1; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 26
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020102(2, 1)
                                        LABEL(255) 254
                        eventdat 2; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 27
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020103(2, 2)
                                        LABEL(255) 254
                        eventdat 3; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 28
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020104(2, 3)
                                        LABEL(255) 254
                        eventdat 4; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 29
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020105(2, 4)
                                        LABEL(255) 254
                        eventdat 5; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 30
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020106(2, 5)
                                        ODirSet(3) 30 0
                                        LABEL(255) 254
                        eventdat 6; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 31
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020107(2, 6)
                                        LABEL(255) 254
                        eventdat 7; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 32
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020108(2, 7)
                                        LABEL(255) 254
                        eventdat 8; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 33
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020109(2, 8)
                                        LABEL(255) 254
                        eventdat 9; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 34
                                        EvFlg_AND(4) (50, 2)
                                        potch(18) 1 7
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020110(2, 9)
                                        TimWait(73) 20
                                        WindowSentaku(40) 0 0 2 1006020115(2, 14) 1006020116(2, 15)
                                        SentakuJump(41) 2 0 1
                                        LABEL(255) 0
                                        WindowSerifu(24) 34 1006020117(2, 16)
                                        SoundCall(101) (4, 7)
                                        SoundCall(101) (4, 7)
                                        OverlayGo(30) 2 4 0 4 48 0
                                        SentakuJump(41) 2 2 3
                                        LABEL(255) 2
                                        PartyMoney(107) 1 7
                                        EvFlgSet(9) (50, 2)
                                        LABEL(255) 254
                                        LABEL(255) 3
                                        LABEL(255) 254
                                        LABEL(255) 1
                                        LABEL(255) 254
                                        LABEL(255) 254
                        eventdat 10; etyp: 1
                                eventform:
                                        EVENT_HUMAN(5) 34
                                        EvFlg_AND(4) (50, 2)
                                        potch(18) 0 7
                                        END(255) 254
                                eventcom:
                                        WindowHenji(23) 1006020110(2, 9)
                                        TimWait(73) 20
                                        WindowSentaku(40) 0 0 2 1006020115(2, 14) 1006020116(2, 15)
                                        SentakuJump(41) 2 0 1
                                        LABEL(255) 0
                                        WindowSerifu(24) 34 1006020121(2, 20)
                                        LABEL(255) 1
                                        LABEL(255) 254
                                        LABEL(255) 255
                                        LABEL(255) 255
                                        LABEL(255) 254
                                        LABEL(255) 254
.....
```

### Misc Notes
- Some Window commands make reference to a (mfno, mno) that don't exist in the sce_msg. I suspect this is a bug in the eventCom itself, as it's a limited issue affecting only a few maps like Trial Road. For now, it outputs a WARN when it detects these.

- EVENT_HUMANs refer to objects on the map. Numbers 0-7 refer to the party.
- LABELs are used as the destination for LabelJump and SentakuJump. LABEL(255) 254 is used as a return.
- When looking up WINDOW_MSG, you may not find it in text_gsd2_en. In that case, also check the text_gsd2_tbl TextAsset, which maps some ids to others due to reuse across maps.

- For descriptions of the commands, please see event_commands/event_com_commands.py and event_commands/event_form_commands.py.

- If you want to parse everything, I recommend downloading git bash and running a command like the following from your exports MonoBehavior directory: `for file in v[a-z][0-9][0-9].json; do echo "Processing $file" >&2; py ../suik_event_parser.py -i $file -t ../TextAsset/text_gsd2_en; done > parsed_events.txt 2>&1`