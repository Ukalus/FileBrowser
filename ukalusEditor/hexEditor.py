import imgui 
import math
class HexEditor:
    filepath: str = ""
    file: str = ""
    byte_array = []
    # lines is how often you can devide the files bytes length by 32  + 1 for files that are not divisible by 32
    lines = 100
    def parse_hex_data(self):
        line_length = 32  # Number of pairs per line
        hex_lines = []
        # Convert each byte to a hex representation
        hex_data = [f"{byte:02X}" for byte in self.byte_array]
        
        # Chunk the hex data into lines of 32 pairs
        for i in range(0, len(hex_data), line_length):
            # Join 32 pairs with spaces, breaking them into 16/16 format visually
            chunk = hex_data[i:i + line_length]
            left = chunk[:16]  # First 16
            right = chunk[16:]  # Last 16
            
            # Join the left and right sections with proper spacing
            line = " ".join(left) + "  " + " ".join(right)
            hex_lines.append(line)
        
        # Print or return the formatted output
        result = "\n".join(hex_lines)
        return result
    def render(self):
        imgui.begin("File:" + self.filepath)
        # Calculate available height
        available_width = imgui.get_content_region_available()[0] / 8  # Remaining width in the window
        available_height = imgui.get_content_region_available()[1]  # Remaining height in the window

        # Adjust list box to fill the remaining space
        imgui.begin_list_box("##List", available_width, available_height)
        for i in range(len(self.byte_array)):
            imgui.selectable(f"0x000{i}", False)
        imgui.end_list_box()
        imgui.same_line()
        
        changed, self.text = imgui.input_text_multiline(
        "##hexbox",  # Invisible label
        self.parse_hex_data(),    # Current content of the text box
        width = available_width * 3,
        height = available_height,
        flags=imgui.INPUT_TEXT_ALLOW_TAB_INPUT
        )
        imgui.same_line()
        changed, self.text = imgui.input_text_multiline(
        "##textbox",  # Invisible label
        self.file,    # Current content of the text box
        # width = available_width * 3,
        height = available_height,
        flags=imgui.INPUT_TEXT_ALLOW_TAB_INPUT
        )

        imgui.end()
    def load_file(self,path: str):
        with open(path, 'rb') as file:
            self.byte_array = bytearray(file.read())  # Read the entire file as a bytearray
             # Print the byte array
        try:
            with open(path, 'r') as file:
                self.file =  file.read()# Read the entire file as a bytearray
                # Print the byte array
        except Exception as e:
            self.file = str(e)