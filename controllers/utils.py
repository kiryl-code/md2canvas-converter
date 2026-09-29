from pathlib import Path

def check_if_directory_exists_and_create(directory_path):
    if not Path(directory_path).exists():
        Path(directory_path).mkdir(parents=True, exist_ok=True)


def save_md_file(file_path, student_id, content):
    full_path = Path(f"{file_path}/{student_id}.md")
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(content)
    return full_path