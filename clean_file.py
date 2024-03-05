def clean_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    # Optionally, replace non-ASCII characters instead of removing them
    clean_content = ''.join(char for char in content if ord(char) < 128)
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(clean_content)

input_file_path = 'notion_content/pikebotwiki.md'
output_file_path = 'notion_content/pikebotwiki.md'

clean_file(input_file_path, output_file_path)