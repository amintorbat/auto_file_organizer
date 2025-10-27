
import os
import shutil
from pathlib import Path

# 📂 دسته‌بندی پسوندها
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv"],
    "Music": [".mp3", ".wav", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java"],
}

def organize_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("❌ مسیر واردشده وجود ندارد!")
        return

    for item in folder.iterdir():
        if item.is_file():
            moved = False
            for category, extensions in FILE_TYPES.items():
                if item.suffix.lower() in extensions:
                    target_dir = folder / category
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(item), str(target_dir / item.name))
                    print(f"📦 {item.name} → {category}/")
                    moved = True
                    break
            if not moved:
                other_dir = folder / "Others"
                other_dir.mkdir(exist_ok=True)
                shutil.move(str(item), str(other_dir / item.name))
                print(f"📦 {item.name} → Others/")

    print("\n✅ پوشه با موفقیت مرتب شد!")

if __name__ == "__main__":
    print("=== 📁 File Organizer ===")
    folder_input = input("مسیر پوشه‌ای که می‌خوای مرتب بشه رو وارد کن: ").strip()
    organize_folder(folder_input)
