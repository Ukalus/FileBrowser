import os
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
from fileExplorer import draw_top_menu, draw_file_tree, render_text_file

selected_file = None  # To store the selected file path

def read_file(file_path: str) -> str:
    """Reads the content of a text file and returns it as a string."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Failed to read file: {str(e)}"

def main():
    global selected_file  # Access the global variable for the selected file
    
    # Initialize GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    # Create a GLFW window
    window = glfw.create_window(800, 600, "ImGui + GLFW Example", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        return

    # Make the OpenGL context current
    glfw.make_context_current(window)

    # Initialize ImGui context
    imgui.create_context()

    # Create a renderer using GLFW
    impl = GlfwRenderer(window)

    # Set the starting directory
    root_path = os.path.abspath("../")  # Example: Start from the parent directory

    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Start a new ImGui frame
        impl.process_inputs()
        imgui.new_frame()
        draw_top_menu()
        new_root_path = draw_file_tree(root_path, selected_file)
        if new_root_path and os.path.isfile(new_root_path):  # If it's a file, update the selected file
            selected_file = new_root_path

        # Display the selected file's content in a text box
        if selected_file and os.path.isfile(selected_file):
            file_content = read_file(selected_file)
            render_text_file(selected_file, file_content)

        # Render ImGui
        imgui.render()
        gl.glClearColor(0.1, 0.1, 0.1, 1)  # Set background color
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        impl.render(imgui.get_draw_data())

        # Swap buffers
        glfw.swap_buffers(window)

    # Cleanup
    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()