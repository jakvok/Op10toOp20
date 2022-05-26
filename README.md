# CNC program convert utility

The script is used to convert CNC programs at Grob G350 5axis milling machine with Siemens Sinumerik 840D control system.
The machine has two clamping systems (palettes) for workpieces. When one of them is inside workarea and workpiece is machined there, the second clamping system is loaded by new workpiece by robot. It saves the cycle time.

Generally, the CNC program is the same for both palettes except G-offsetts, palette-dependent subroutines and probing cycles. The convert utility presented here can convert CNC program debuged at one palette to CNC program suitable for the second palette. It avoids to make boring and possibly faulty human work, manually CNC program conversion.

# Using of the script
Before use make sure the file `changes.csv` is located in the same folder as the script.
In the file `changes.csv` there are stored pairs of values for substitution. If desired, by editing the file is possible to change, delete or add next values for substitution.
Each line of file is reserved for one pair of values separated by comma. The first value is which will be replaced by the second value.

## linux
Python 3.8+, only standard modules required on linux.<br>
Make the script executable:<br>
`$ chmod +x ./Op10toOp20.py`

Run the script:<br>
`$ ./Op10toOp20.py`

## windows
When python 3.8+ installed, using is the same as on linux system.

Or when python is not available on your win system, use the standalone executable `Op10toOp20.exe`.<br>

# Example files
File `example_NC.MPF` is file before conversion.<br>
File `converted_example_NC.MPF` is file after conversion.<br>