import os
from tools.sandbox import run_code_tool

def main():
    print("--- Testing Python Execution ---")
    python_code = """import sys
user_input = sys.stdin.read().strip()
print(f"Received input: {user_input}")
"""
    python_result = run_code_tool(
        code_string=python_code,
        language="python",
        test_case_input="Hello from Python test case!",
        time_limit=2.0
    )
    print(python_result)

    print("\n--- Testing C++ Execution ---")
    cpp_code = """#include <iostream>
#include <string>

int main() {
    std::string input;
    std::getline(std::cin, input);
    std::cout << "Hello World! Input was: " << input << std::endl;
    return 0;
}
"""
    cpp_result = run_code_tool(
        code_string=cpp_code,
        language="cpp",
        test_case_input="C++ Test Input",
        time_limit=2.0
    )
    print(cpp_result)

if __name__ == "__main__":
    main()
