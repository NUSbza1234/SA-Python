import os

def replace_in_file(file_path, search_text, replace_text):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace(search_text, replace_text)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def rename_in_directory(directory, search_text, replace_text):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                replace_in_file(file_path, search_text, replace_text)

if __name__ == '__main__':
    base_dir = 'D:/NUS/Miscellaneous/TADashboard/custom_pandas_ta'  # Update this to your directory
    rename_in_directory(base_dir, 'pandas_ta', 'custom_pandas_ta')
