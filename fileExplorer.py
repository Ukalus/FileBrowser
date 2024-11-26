import os
import imgui
import glfw

def render_file_tree_compontent(path: str):
    imgui.begin("Filebrowser", True)
    draw_file_tree(path)
    imgui.end()
import os
import imgui


def draw_file_tree(path: str, selected_file):
    """
    Recursively render a file tree structure inside an ImGui window.
    :param path: The root path to render.
    :param selected_file: The currently selected file.
    """
    current_path = os.path.abspath(path)

    try:
        # List directory contents
        for entry in os.scandir(current_path):
            if entry.is_dir():
                # Render directory as a tree node with unique IDs
                if imgui.tree_node(entry.name):
                    # Recursively draw subdirectories
                    selected_file = draw_file_tree(entry.path, selected_file)  # Update selected file
                    imgui.tree_pop()  # Always pop the tree node after recursion
            else:
                # Render files as selectable items
                clicked, _ = imgui.selectable(entry.name)
                if clicked:
                    selected_file = entry.path  # Update selected file when clicked
    except PermissionError:
        imgui.text_colored("Permission Denied", 1.0, 0.0, 0.0)  # Handle restricted access

    return selected_file  # Return the updated selected file


def draw_top_menu():
    # Start the main menu bar
    if imgui.begin_main_menu_bar():
        # File Menu
        if imgui.begin_menu("File"):
            # Dropdown items under the File menu
            if imgui.menu_item("Example 1"):
                print("Example 1 selected")
            if imgui.menu_item("Example 2"):
                print("Example 2 selected")
            if imgui.menu_item("Example 3"):
                print("Example 3 selected")
            if imgui.menu_item("Example 4"):
                print("Example 4 selected")
            imgui.end_menu()

        # View Menu
        if imgui.begin_menu("View"):
            if imgui.menu_item("Toggle Fullscreen"):
                print("Fullscreen toggle clicked")
            imgui.end_menu()

        # Help Menu
        if imgui.begin_menu("Help"):
            if imgui.menu_item("About"):
                print("About menu item clicked")
            imgui.end_menu()

        imgui.end_main_menu_bar()

def render_text_file(selected_file, file_content):
    imgui.begin("File Viewer")
    imgui.text(f"Viewing file: {selected_file}")
    imgui.separator()
    imgui.input_text_multiline("##FileContent", file_content, width=1000, height=1000)
    imgui.end()