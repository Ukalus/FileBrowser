
class FileHandler:
    file_name: str
    file: [bytes]
    file_endings: List[str] = [
        ".narc",
        ".bin",
        # TODO add full list of file endings
    ]
    magic_numbers: List[bytes] = [
        b'\x89\x50\x4E\x47',  # PNG
        b'\xFF\xD8\xFF\xE0',  # JPEG
        b'\x25\x50\x44\x46',  # PDF
        b'\x50\x4B\x03\x04'   # ZIP
        # TODO add full list of magic numbers

]

    def check_magic_number(file_path, known_magic_numbers):
    try:
        with open(file_path, 'rb') as file:  # Open the file in binary mode
            # Read the maximum number of bytes required for comparison
            max_bytes = max(len(magic) for magic in known_magic_numbers)
            file_magic = file.read(max_bytes)
            
            # Check against each known magic number
            for magic_number in known_magic_numbers:
                if file_magic.startswith(magic_number):
                    return f"Match found: {magic_number.hex()}"
            
            return "No match found."
    except FileNotFoundError:
        return "File not found."
    except IOError as e:
        return f"An error occurred: {e}"

from typing import List

# Define a list of byte sequences

