from functions.get_files_info import get_files_info

def main():
    cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]

    for working_dir, directory in cases:
        result = get_files_info(working_dir, directory)
        print(f'get_files_info("{working_dir}", "{directory}"):')
        for line in result.splitlines():
            print(f"    {line}")
        print()

if __name__ == "__main__":
    main()