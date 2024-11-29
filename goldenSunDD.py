

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
        print(indent + file + " (File)")
index = 0
print_folder(index, root_folder)


# Function to recreate the folder structure and write file data
def create_folder_structure_with_full_path(index, input_folder, current_path, output_base, rom, max_depth=4):
    if index >= max_depth:
        return

    index += 1

    # Iterate through folders
    for folder in input_folder.folders:
        folder_path = os.path.join(output_base, folder[0])  # Path where folder will be created
        os.makedirs(folder_path, exist_ok=True)  # Create the folder
        print(f"Created folder: {folder_path}")  # Optional: print for debugging

        # Construct the new path for the folder in the ROM
        new_rom_path = os.path.join(current_path, folder[0])

        # Recursive call
        create_folder_structure_with_full_path(index, folder[1], new_rom_path, folder_path, rom, max_depth)

    # Iterate through files
    for file in input_folder.files:
        # Construct the full ROM path for the file
        full_rom_path = os.path.join(current_path, file)

        # Construct the output file path
        file_path = os.path.join(output_base, file)

        try:
            # Get the binary data for the file using the full ROM path
            file_data = rom.getFileByName(full_rom_path)

            # Write binary data to the output file
            with open(file_path, "wb") as f:
                f.write(file_data)
            print(f"Created file with data: {file_path}")  # Optional: print for debugging
        except Exception as e:
            print(f"Error writing file {file}: {e}")  # Handle errors gracefully

# Base output folder where structure will be created
output_base = os.path.join(os.getcwd(), "ROM_Folder_Structure_With_Full_Path")  # Adjust as needed
os.makedirs(output_base, exist_ok=True)  # Ensure the base folder exists

# Start creating the folder structure with file data
index = 0
create_folder_structure_with_full_path(
    index=index,
    input_folder=root_folder,
    current_path="",  # Start with the root folder of the ROM
    output_base=output_base,
    rom=rom
)