import os
import imgui
import glfw
import pyperclip
from ukalusEditor.addons.goldenSunDD.rom import Rom_DD
from ukalusEditor.hexEditor import HexEditor

class MainMenuUI:
    open_new_file_dialog = False
    open_select_folder_dialog = False
    open_rom_export_dialog = False
    new_root_path = os.path.abspath("./")
    root_path = os.path.abspath("./")
    export_rom_path = os.path.abspath("./") + "/rom_fs"
    selected_file = ""
    rom_dd = rom_dd = Rom_DD()
    hex_editor = HexEditor()
    new_file_selected = False
    new_file_path = ""
    new_file_path_init = True
    debug_show = False
    open_open_file_dialog = False
    input_file_open_open_file_dialog = os.path.abspath("./")
    new_rename_file_name = ""
    old_rename_file_name = ""
    open_rename_file_dialog = False

    def debug_show_state(self):
        imgui.begin("Debug menu")
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
                widget_id = entry.path
                if entry.is_dir():
                    # Render directory as a tree node with unique IDs
                    if imgui.tree_node(entry.name):
                        if imgui.begin_popup_context_item(widget_id):
                            if imgui.menu_item("Open folder")[0]:
                                self.root_path = entry.path
                            if imgui.menu_item("Copy absolute path")[0]:
                                pyperclip.copy(entry.path)
                            if imgui.menu_item("Rename")[0]:
                                print("Specific Option 3 selected")
                            if imgui.menu_item("Delete")[0]:
                                print("Specific Option 4 selected")
                            imgui.end_popup()
                        # Recursively draw subdirectories
                        self.draw_file_tree(entry.path)  # Update selected file
                        imgui.tree_pop()  # Always pop the tree node after recursion
                else:
                    # Render files as selectable items
                    clicked, _ = imgui.selectable(entry.name, self.selected_file == entry.path)
                    if imgui.begin_popup_context_item(widget_id):
                        if imgui.menu_item("Open")[0]:
                            self.selected_file = entry.path
                            self.new_file_selected = True
                        if imgui.menu_item("Copy absolute path")[0]:
                            pyperclip.copy(entry.path)
                        if imgui.menu_item("Rename")[0]:

                            self.open_rename_file_dialog = True
                            self.old_rename_file_name = entry.path
                            self.new_rename_file_name = self.old_rename_file_name
                        if imgui.menu_item("Delete")[0]:
                            print("Specific Option 4 selected")
                        imgui.end_popup()
                    if clicked:
                        self.selected_file = entry.path  # Update selected file when clicked
                        self.new_file_selected = True
                    
                   
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
                    self.open_open_file_dialog = True

                open_folder_clicked, _ = imgui.menu_item("Open folder")
                if open_folder_clicked:
                    self.open_select_folder_dialog = True
                imgui.end_menu()

            # View Menu
            if imgui.begin_menu("View"):
                toggle_fullscreen_clicked, _ = imgui.menu_item("Toggle Fullscreen")
                if toggle_fullscreen_clicked:
                    print("Fullscreen toggle clicked")
                imgui.end_menu()

            # Help Menu
            if imgui.begin_menu("Help"):
                open_debug_clicked, _ = imgui.menu_item("Open debug menu")
                if open_debug_clicked:
                    self.debug_show = not self.debug_show
                imgui.end_menu()

            # Addons Menu
            if imgui.begin_menu("Addons"):
                if imgui.begin_menu("Golden Sun: Dark Dawn"):
                    open_rom_clicked, _ = imgui.menu_item("Open Rom")
                    if open_rom_clicked:
                        self.open_rom_export_dialog = True
                    option_2_clicked, _ = imgui.menu_item("Enemies")
                    if option_2_clicked:
                        print("Option 2 selected")
                    option_3_clicked, _ = imgui.menu_item("Party")
                    if option_3_clicked:
                        print("Option 3 selected")
                    option_4_clicked, _ = imgui.menu_item("Loot Tables")
                    if option_4_clicked:
                        print("Option 3 selected")
                    imgui.end_menu()

            imgui.end_main_menu_bar()

        if self.debug_show:
            self.debug_show_state()
        # Handle dialogs for "New File", "Open Folder", and "Open ROM"
        if self.open_new_file_dialog: 
            if self.new_file_path_init:
                if len(self.selected_file) > 0:
                    self.new_file_path = self.selected_file[:self.selected_file.rfind('/')+1]
                elif len(self.root_path) > 0:
                    self.new_file_path = self.root_path
                else:
                    self.new_file_path = ""
                self.new_file_path_init = False
            imgui.begin("Confirm New File Creation")

            imgui.text("Do you want to create a new file?")
            

            changed, self.new_file_path = imgui.input_text("new file path:", self.new_file_path)
            if imgui.button("Yes"):
                print("new:" + self.new_file_path)
                with open(self.new_file_path,'w') as file:
                    pass  # No content is written; the file is created empty
                print("New file created!")  # Replace with actual file creation logic
                self.open_new_file_dialog = False  # Close the dialog
                self.new_file_path_init = True
            imgui.same_line()  # Place the buttons next to each other
            if imgui.button("No"):
                self.open_new_file_dialog = False  # Close the dialog
                self.new_file_path_init = True
            imgui.end()
        if self.open_open_file_dialog:
            imgui.begin("Open File")
            imgui.text("Enter File path")
            changed, self.input_file_open_open_file_dialog = imgui.input_text("path:", self.input_file_open_open_file_dialog)
            imgui.text(self.input_file_open_open_file_dialog)
            if imgui.button("Open"):
                self.selected_file = self.input_file_open_open_file_dialog
                self.new_file_selected = True
                self.open_open_file_dialog = False
            imgui.end()
        if self.open_select_folder_dialog:
            imgui.begin("Open folder")
            imgui.text("Enter File path")
            changed, self.new_root_path = imgui.input_text("path:", self.new_root_path)
            imgui.text(self.new_root_path)
            if imgui.button("Open"):
                self.root_path = self.new_root_path
                self.open_select_folder_dialog = False
            imgui.end()
        if self.open_rename_file_dialog:
            imgui.begin("rename folder")
            changed, self.old_rename_file_name = imgui.input_text("file:", self.old_rename_file_name)
            changed, self.new_rename_file_name = imgui.input_text("new name:", self.new_rename_file_name)
            if imgui.button("Rename"):
                print("Renamed!")
                print("from:" + self.old_rename_file_name)
                print("to:" + self.new_rename_file_name)
                os.rename(self.old_rename_file_name,self.new_rename_file_name)
                self.open_rename_file_dialog = False
            imgui.end()
        if self.open_rom_export_dialog:
            imgui.begin("Open ROM")

            imgui.text("Enter ROM path")
            changed_input_path, self.new_root_path = imgui.input_text("in_path:", self.new_root_path)

            imgui.text("Export path")
            changed_output_path, self.export_rom_path = imgui.input_text("out_path:", self.export_rom_path)

            if imgui.button("Unpack ROM"):
                self.rom_dd.set_input_path("/home/ukalus/Schreibtisch/goldenSunDD.nds")
                self.rom_dd.set_output_path(self.export_rom_path)
                self.rom_dd.export_rom_fs()
                self.root_path = self.export_rom_path
                self.open_rom_export_dialog = False
            imgui.end()

    def handle_file(self):
        if self.new_file_selected:
            print("file changed:" + self.selected_file)
            self.hex_editor.load_file(self.selected_file)
        self.hex_editor.render()
        self.hex_temp_file = self.selected_file
        self.new_file_selected = False
