from functions.get_file_content import get_file_content

def main():
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print()

    test_cases = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
    ]

    for working_dir, file_path in test_cases:
        result = get_file_content(working_dir, file_path)
        print(f'get_file_content("{working_dir}", "{file_path}"):')
        print(result)
        print()

if __name__ == "__main__":
    main()
