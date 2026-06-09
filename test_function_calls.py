from functions.get_file_content import get_file_content
from functions.write_file_content import write_file
from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info


print(get_file_content('file_path', 'main.py'))
print(write_file('calculator', 'main.txt', 'hello'))
print(run_python_file('file_path', 'main.py'))
print(get_files_info('directory', 'pkg'))