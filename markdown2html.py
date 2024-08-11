#!/usr/bin/python3
"""
A script that converts markdown to HTML.
"""
import sys
import os
import re

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
            for line in file_1:
                line = line.rstrip()  # Safely strip trailing whitespace including newline
                match = re.match(r'^(#{1,6})\s+(.*)', line)
                if match:
                    h_level = len(match.group(1))
                    heading_text = match.group(2)
                    html_content.append(f'<h{h_level}>{heading_text}</h{h_level}>\n')
                else:
                    html_content.append(line + '\n')

        with open(output_file, 'w', encoding='utf-8') as file_2:
            file_2.writelines(html_content)

    except IOError as e:
        print(f'Error reading/writing file: {e}', file=sys.stderr)
        sys.exit(1)
