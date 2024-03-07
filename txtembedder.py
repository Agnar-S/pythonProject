import os
import openai
# Set your OpenAI API key here (preferably, it should be set as an environment variable)
from openai import OpenAI

import constants
import usercall as uc


# Directory where your 92 text files are stored
directory_path = '/Users/ap/PycharmProjects/smartpackproject/data'

# Path for the new aggregated text file
output_file_path = 'test.txt'

# Open the output file in write mode
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Ensure to process only text files
            file_path = os.path.join(directory_path, filename)

            # Open and read the contents of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                # Read the content, replacing any newlines with spaces
                content = file.read()
                processed_content = uc.api_call(content, "asst_bCgyobnuzVlIig6TWQoGkgb3")

                # Write the content as a single line in the output file
                # Add a newline character at the end to start a new line for the next file's content
                output_file.write(processed_content + "\n")

print("All text files have been compiled into:", output_file_path)
