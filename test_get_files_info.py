# Import the function from the 'functions' subdirectory
from functions.get_files_info import get_files_info

# Print the results of the test cases
print("Result for current directory:")
print(get_files_info("calculator", "."))

print("\nResult for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))

print("\nResult for '/bin' directory:")
print(get_files_info("calculator", "/bin"))

print("\nResult for '../' directory:")
print(get_files_info("calculator", "../"))