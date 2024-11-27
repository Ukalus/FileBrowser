import os
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
from fileExplorer import MainMenuUI

def main():
    
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
    mainMenuUI = MainMenuUI()
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Start a new ImGui frame
        impl.process_inputs()
        imgui.new_frame()
        mainMenuUI.draw_top_menu()
        mainMenuUI.render_file_tree_compontent()
        mainMenuUI.render_text_file()
        # mainMenuUI.debug_show_state()

        # Display the selected file's content in a text box
        

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