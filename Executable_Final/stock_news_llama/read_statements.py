import pandas as pd
import os
import csv

folder_path = "questions_data/"
output_folder = os.path.join( "statement_txt")
# output_txt = "output_headings.txt"

import os
import csv

def extract_headings_and_text(csv_file):
    headings_and_text = set()
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Concatenate heading and text and add to the set
            heading_and_text = f"{row['heading']} {row['text']}"
            headings_and_text.add(heading_and_text)
    return headings_and_text

def extract_txt(folder_path, output_txt):
    output_txt = os.path.join(output_folder, "output_headings_and_text.txt")
    processed_files = set()

    # Check if the output file already exists
    if os.path.exists(output_txt):
        with open(output_txt, 'r', encoding='utf-8') as file:
            processed_files = set(file.read().splitlines())

    with open(output_txt, 'a', encoding='utf-8') as out_file:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv') and file_name not in processed_files:
                file_path = os.path.join(folder_path, file_name)
                headings_and_text = extract_headings_and_text(file_path)

                # Write unique headings and text combinations to the output file
                for heading_and_text in headings_and_text:
                    out_file.write(heading_and_text + '\n')

                # Mark the file as processed
                processed_files.add(file_name)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

extract_txt(folder_path, output_folder)