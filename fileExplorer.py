import os
import imgui
import glfw
from goldenSunDD import Rom_DD

class MainMenuUI:
    open_new_file_dialog = False
    open_select_folder_dialog = False
    open_rom_export_dialog = False
    new_root_path = os.path.abspath("./")
    root_path = os.path.abspath("./")
    export_rom_path = os.path.abspath("./") + "/rom_fs"
    selected_file = ""
    rom_dd = rom_dd = Rom_DD()

    def debug_show_state(self):
        imgui.begin("debug main menu")
        imgui.text("open_new_file_dialog:" + str(self.open_new_file_dialog))
        imgui.input_text("root_path:", self.root_path)
        imgui.input_text("new_root_path:", self.new_root_path)
        imgui.input_text("selected_file:", self.selected_file)
        imgui.end()
    def render_file_tree_compontent(self):
        imgui.begin("Filebrowser", True)
        self.draw_file_tree(self.root_path)
        imgui.end()

    def read_file(self,file_path: str) -> str:
        """Reads the content of a text file and returns it as a string."""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Failed to read file: {str(e)}"


    def draw_file_tree(self,path: str):
        """
        Recursively render a file tree structure inside an ImGui window.
        :param path: The root path to render.
        :param selected_file: The currently selected file.
        """


        try:
            # List directory contents
            for entry in os.scandir(path):
                if entry.is_dir():
                    # Render directory as a tree node with unique IDs
                    if imgui.tree_node(entry.name):
                        # Recursively draw subdirectories
                        self.draw_file_tree(entry.path)  # Update selected file
                        imgui.tree_pop()  # Always pop the tree node after recursion
                else:
                    # Render files as selectable items
                    clicked, _ = imgui.selectable(entry.name)
                    if clicked:
                        self.selected_file = entry.path  # Update selected file when clicked
        except PermissionError:
            imgui.text_colored("Permission Denied", 1.0, 0.0, 0.0)  # Handle restricted access

    def draw_top_menu(self):
        # Start the main menu bar
        if imgui.begin_main_menu_bar():
            # File Menu
            if imgui.begin_menu("File"):
                # Dropdown items under the File menu
                new_file_clicked, _ = imgui.menu_item("New File")
                if new_file_clicked:
                    self.open_new_file_dialog = True

                open_file_clicked, _ = imgui.menu_item("Open File")
                if open_file_clicked:
                    print("Example 2 selected")

                open_folder_clicked, _ = imgui.menu_item("Open folder")
                if open_folder_clicked:
                    self.open_select_folder_dialog = True

                open_rom_clicked, _ = imgui.menu_item("Open Rom")
                if open_rom_clicked:
                    self.open_rom_export_dialog = True
                imgui.end_menu()

            # View Menu
            if imgui.begin_menu("View"):
                toggle_fullscreen_clicked, _ = imgui.menu_item("Toggle Fullscreen")
                if toggle_fullscreen_clicked:
                    print("Fullscreen toggle clicked")
                imgui.end_menu()

            # Help Menu
            if imgui.begin_menu("Help"):
                about_clicked, _ = imgui.menu_item("About")
                if about_clicked:
                    print("About menu item clicked")
                imgui.end_menu()

            imgui.end_main_menu_bar()
        if self.open_new_file_dialog: 
            imgui.begin("Confirm New File Creation")

            imgui.text("Do you want to create a new file?")
            new_file_path = self.selected_file
            imgui.input_text("path:", new_file_path)
            if imgui.button("Yes"):
                print("New file created!")  # Replace with actual file creation logic
                self.open_new_file_dialog = False  # Close the dialog
            imgui.same_line()  # Place the buttons next to each other
            if imgui.button("No"):
                self.open_new_file_dialog = False  # Close the dialog
            imgui.end()
        if self.open_select_folder_dialog:
            imgui.begin("Open File")
            imgui.text("Enter File path")
            changed,self.new_root_path = imgui.input_text("path:", self.new_root_path)
            imgui.text(self.new_root_path)
            if imgui.button("Open"):
                print("ukalus:" + self.new_root_path)
                self.root_path = self.new_root_path
                self.open_select_folder_dialog = False
            imgui.end()

        if self.open_rom_export_dialog:
            imgui.begin("Open ROM")
            
            imgui.text("Enter ROM path")
            changed_input_path,self.new_root_path = imgui.input_text("in_path:", self.new_root_path)

            imgui.text("Export path")
            changed_output_path,self.export_rom_path = imgui.input_text("out_path:", self.export_rom_path)
            
            if imgui.button("Unpack ROM"):
                self.rom_dd.set_input_path("/home/ukalus/Schreibtisch/goldenSunDD.nds")
                self.rom_dd.set_output_path(self.export_rom_path)
                self.rom_dd.export_rom_fs()
                self.root_path = self.export_rom_path
                self.open_rom_export_dialog = False
            imgui.end()
        

    def render_text_file(self):
        if self.selected_file and os.path.isfile(self.selected_file):
            file_content = self.read_file(self.selected_file)
            imgui.begin("File Viewer", True)
            imgui.text(f"Viewing file: {self.selected_file}")
            imgui.separator()
            imgui.input_text_multiline("##FileContent", file_content, width=1000, height=1000)
            imgui.end()