## Overview

This documents the steps to get started with reverse engineering the Suikoden I & II Remaster (an IL2CPP Unity game) using Ghidra and Il2CppInspectorRedux.

Note: these steps take a long time to run, likely 2+ hours depending on your machine's horsepower. 

## Prereqs

Download the latest from:

- https://github.com/LukeFZ/Il2CppInspectorRedux (I used https://github.com/LukeFZ/Il2CppInspectorRedux/tree/ec76447122d92967b14db1246002408120417d26)
- https://github.com/NationalSecurityAgency/ghidra (I used the 11.3.2 release)

## Running Il2CppInspectorRedux

1) Build via the instructions in its README.md:

```
dotnet publish -c Release
powershell -f get-plugins.ps1
```

If publish fails for VersionedSerialization.Generator, apply the fix from https://github.com/LukeFZ/Il2CppInspectorRedux/issues/14

2) Copy the `plugins` directory to  `Il2CppInspector.CLI\bin\Release\net9.0\win-x64`
3) From a command line, run the CLI:
```
cd Il2CppInspector.CLI\bin\Release\net9.0\win-x64

.\Il2CppInspector.exe -i "E:\SteamLibrary\steamapps\common\Suikoden I and II HD Remaster\GameAssembly.dll" -m "E:\SteamLibrary\steamapps\common\Suikoden I and II HD Remaster\Suikoden I and II HD Remaster_Data\il2cpp_data\Metadata\global-metadata.dat" --unity-version 2022.3.28f1  -t Ghidra
```

(replace `E:\SteamLibrary\steamapps\common\Suikoden I and II HD Remaster` with your game directory)

Results:

- `Il2CppInspector.CLI\bin\Release\net9.0\win-x64` contains `il2cpp.py` (you won't use this) and `metadata.json` (you'll copy this below)
- `Il2CppInspector.CLI\bin\Release\net9.0\win-x64\cpp\appdata` contains `il2cpp-types.h` (you'll need this below)


## Running Ghidra

1) Start Ghidra using the `support\pyghidraRun.bat` script. Ref: https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PyGhidra/README.md
2) _File_ -> _Import File_. Choose `Suikoden I and II HD Remaster\GameAssembly.dll`
3) Default options will work (`x86:LE:64:default` visualstudio Windows PE)
4) As instructed by https://github.com/LukeFZ/Il2CppInspectorRedux/blob/master/README.md#adding-metadata-to-your-ghidra-workflow:
   1) From the _Code Browser_, choose _File -> Parse C Source..._
   2) Create a new profile and add the generated C++ type header file. This is `cpp\appdata\il2cpp-types.h`
   3) Ensure the _Parse Options_ are set exactly as follows: `-D_GHIDRA_`
   4) Click _Parse to Program_ and accept any warnings. This will take a while to complete.
   5) For steps 5 - 8, use the `il2cpp_py3_win64.py` from this repo instead of the generated `il2cpp.py`. Notes:
      - You'll need to copy the earlier generated `metadata.json` to wherever you're running `il2cpp_py3_win64.py`.
      - There are currently some exceptions re: demangled names that can be ignored. 
      - It will take a while to complete (32 minutes on my box).
5) _Analysis_ -> _Analyze All Open_. Run the default options. This will take a while to run.

And good luck. Reverse Engineering with Ghidra can be extremely challenging but rewarding.

If you find anything useful, please post to the suikoden-mod-dev channel on the Moogles & Mods discord: https://discord.gg/4HcbJx58


## Misc notes

I recommend following this guide to improve the Ghidra experience: https://www.embeeresearch.io/understanding-and-improving-ghidra-ui-for-malware-analysis/

I originally used Il2CppDumper and followed https://gist.github.com/BadMagic100/47096cbcf64ec0509cf75d48cfbdaea5. However, I found the resulting Discompilation of key methods lacking important struct definitions and requiring convoluted redirection within the structs themselves, leading me to seek out alternatives to Il2CppDumper.