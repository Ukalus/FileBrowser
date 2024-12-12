import os
import ndspy.rom
import ndspy.fnt


class Rom_DD:
    #'/home/ukalus/Schreibtisch/goldenSunDD.nds'
    # Load the NDS ROM
    input_path = ""
    output_path = ""
    
    rom = ""
    root_folder = ""
    depth = 0
    current_path = ""

    # Function to recreate the folder structure and write file data
    def export_rom_fs(self):
        self.create_folder_structure_with_full_path(
            index=self.depth,
            input_folder=self.root_folder,
            current_path=self.current_path,  # Start with the root folder of the ROM
            output_base=self.output_path,
            rom=self.rom
        )
    def set_input_path(self,path: str):
        self.input_path = path
        self.rom = ndspy.rom.NintendoDSRom.fromFile(self.input_path)
        self.root_folder = self.rom.filenames
    def set_output_path(self,path: str):
        self.output_path = os.path.join(os.getcwd(), path)
        os.makedirs(self.output_path, exist_ok=True)
    def create_folder_structure_with_full_path(self,index, input_folder, current_path, output_base, rom, max_depth=100):
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
            self.create_folder_structure_with_full_path(index, folder[1], new_rom_path, folder_path, rom, max_depth)

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


# rom_dd = Rom_DD()
# rom_dd.set_input_path("/home/ukalus/Schreibtisch/goldenSunDD.nds")
# rom_dd.set_output_path("out12")
# rom_dd.export_rom_fs()

