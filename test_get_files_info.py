from functions.get_files_info import get_files_info
import os
import functions.get_files_info
print("Using get_files_info from:", functions.get_files_info.__file__)

print('--- Test 1: "."')
print("Result for current directory:")
result1 = get_files_info("calculator", ".")
print(result1)

print('\n--- Test 2: "pkg"')
print("Result for 'pkg' directory:")
result2 = get_files_info("calculator", "pkg")
print(result2)

print('\n--- Test 3: "/bin"')
print("Result for '/bin' directory:")
result3 = get_files_info("calculator", "/bin")
print(result3)

print('\n--- Test 4: "../"')
print("Result for '../' directory:")
result4 = get_files_info("calculator", "../")
print(result4)

