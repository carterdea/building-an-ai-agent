from functions.run_python import run_python_file

# Test 1: Run main.py without arguments (should show usage)
result = run_python_file("calculator", "main.py")
print("Test run_python_file('calculator', 'main.py'):")
print(result)

print()

# Test 2: Run main.py with calculator expression
result = run_python_file("calculator", "main.py", ["3 + 5"])
print("Test run_python_file('calculator', 'main.py', ['3 + 5']):")
print(result)

print()

# Test 3: Run tests.py (note: this might cause recursion)
result = run_python_file("calculator", "tests.py")
print("Test run_python_file('calculator', 'tests.py'):")
print(result)

print()

# Test 4: Try to run file outside working directory
result = run_python_file("calculator", "../main.py")
print("Test run_python_file('calculator', '../main.py'):")
print(result)

print()

# Test 5: Try to run non-existent file
result = run_python_file("calculator", "nonexistent.py")
print("Test run_python_file('calculator', 'nonexistent.py'):")
print(result)
