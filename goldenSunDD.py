

import os
import ndspy.rom
import ndspy.fnt

# Load the NDS ROM
output_path = 'output_folder'  # Replace with your desired output folder
rom = ndspy.rom.NintendoDSRom.fromFile('/home/ukalus/Schreibtisch/goldenSunDD.nds')

root_folder = rom.filenames

# Print the contents of the root folder
def print_folder(index, input_folder, max_depth=2):
    if index >= max_depth:
        return

    index = index + 1
    indent = "   " * index + "> " 
    
    for folder in input_folder.folders:
        print(indent + folder[0])
        print_folder(index, folder[1])
    for file in input_folder.files:                
        print(indent + file)
index = 0
print_folder(index, root_folder)
