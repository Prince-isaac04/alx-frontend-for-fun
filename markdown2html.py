#!/usr/bin/python3
"""
A script that converts markdown to HTML.
"""
import sys
import os
import re
import hashlib

def replace_bold_italic(line):
    # Replace **text** with <b>text</b>
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    # Replace __text__ with <em>text</em>
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
    return line

def replace_private_content(line):
    # Replace [[private]] with a hash value
    return re.sub(r'\[\[(.*?)\]\]', lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), line)

def replace_text_patterns(line):
    # Replace ((text)) with an empty string (as an example)
    line = re.sub(r'\(\((.*?)\)\)', '', line)
    return line

if __name__ == '__main__':

    # Test that the number of arguments passed is 2
    if len(sys.argv) != 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check that the markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, encoding='utf-8') as file_1:
            html_content = []
            in_list = False
            for line in file_1:
                line = line.rstrip()  # Safely strip trailing whitespace including newline

                # Handle headings
                match = re.match(r'^(#{1,6})\s+(.*)', line)
                if match:
                    h_level = len(match.group(1))
                    heading_text = match.group(2)
                    html_content.append(f'<h{h_level}>{heading_text}</h{h_level}>\n')
                    continue

                # Handle list items
                if line.startswith('- '):
                    if not in_list:
                        html_content.append('<ul>\n')
                        in_list = True
                    item_text = line[2:]
                    item_text = replace_bold_italic(item_text)
                    item_text = replace_private_content(item_text)
                    item_text = replace_text_patterns(item_text)
                    html_content.append(f'<li>{item_text}</li>\n')
                    continue
                else:
                    if in_list:
                        html_content.append('</ul>\n')
                        in_list = False

                # Handle bold/italic text and custom patterns
                line = replace_bold_italic(line)
                line = replace_private_content(line)
                line = replace_text_patterns(line)

                # Handle paragraphs
                if line.strip() != "":
                    html_content.append(f'<p>\n{line}\n</p>\n')

            if in_list:  # Close any open list at the end
                html_content.append('</ul>\n')

        with open(output_file, 'w', encoding='utf-8') as file_2:
            file_2.writelines(html_content)

    except IOError as e:
        print(f'Error reading/writing file: {e}', file=sys.stderr)
        sys.exit(1)
