from functions.get_files_info import get_files_info

def main():
    # Test cases
    cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]

    for working_dir, directory in cases:
        result = get_files_info(working_dir, directory)
        # Print in the required format
        print(f'get_files_info("{working_dir}", "{directory}"):')
        # Indent each line of the result
        for line in result.splitlines():
            print(f"    {line}")
        print()  # blank line between cases

if __name__ == "__main__":
    main()