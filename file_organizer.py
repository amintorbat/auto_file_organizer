
import os
import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from tqdm import tqdm

@dataclass
class FileInfo:
    name : str
    path: Path
    size: int
    modified: datetime
    extension : str
    selected: bool = False


history = []


# -- languages --
messages = {
    "fa" : {
        "select_lang": "زبان را انتخاب کنید(fa/en):",
        "welcome": "خوش آمدید به برنامه",
        "path_input" : "آدرس پوشه ای را که میخواهید مرتب شود را وارد کنید :",
        "use_default" : "آیا میخواهید از دسته بندی پیش فرض استفاده کنید؟ (y/n):",
        "customm_prompt" :"نام پوشه و پسوند مربوطه را  وارد کنید(مثلا : عکسjpg,png): ",
        "choose_sort": "روش مرتب‌سازی را انتخاب کنید:\n1. نوع فایل\n2. تاریخ\n3. اندازه فایل\n> ",
        "done": "مرتب سازی با موفقیت انجام شد ✅",
        "invalid_path": "آدرس وارد شده معتبر نیست ❌",
        "organizing" : "در حال مرتبسازی فایل ها...",
        "undo_done": "آخرین عملیات با موفقیت بازگردانده شد 🔄",
        "no_undo": "هیچ عملی برای بازگردانی وجود ندارد ⚠️",
        "report": "\n📊 گزارش عملکرد:\n- فایل‌ها: {files}\n- حجم جابه‌جا شده: {size:.2f} MB\n- زمان اجرا: {time:.2f} ثانیه\n"
    },
    "en" : {
        "select_lang" : "Select language (fa/en): ",
        "welcome" : "Welcome to Auto File Organizer ",
        "path_input" : "Enter the folder path to organize: ",
        "use_default" : "Do you want to use the default categories? (y/n)",
        "custom_prompt" : "Enter folder name and extensions (e.d., Images jpg,png): ",
        "choose_sort": "Choose sorting method:\n1. File Type\n2. Date\n3. File Size\n> ",
        "done": "File organized successfully ✅",
        "invalid_path" : "Invalid folder path ❌",
        "organizing": "Organizing files...",
        "undo_prompt": "Do you want to undo the last action? (y/n): ",
        "undo_done": "Last action undone successfully 🔄",
        "no_undo": "No actions to undo ⚠️",
        "report": "\n📊 Report:\n- Files: {files}\n- Total moved: {size:.2f} MB\n- Time taken: {time:.2f} sec\n"
    }
}



# Extensions category 📂
default_categories = {
    "Images": ["jpg", "jpeg", "png", "gif", "bmp"],
    "Videos": ["mp4", "mkv", "mov", "avi"],
    "Documents": ["pdf", "docx", "txt", "xlsx"],
    "Audio": ["mp3", "wav", "ogg"],
    "Archives": ["zip", "rar", "7z"],
    "Code": ["py", "js", "html", "css", "cpp", "c", "java"],
}


# sorting by file type
def organize_by_type(folder_path, categories, lang):
    start_time = datetime.now()
    total_size = 0
    count = 0
    print(messages[lang]["organizing"])


    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for filename in tqdm(files, desc="Processing", ncols=80):
        file_path = os.path.join(folder_path, filename)


        ext = filename.split(".")[-1].lower()
        for category, extensions in categories.items():
            if ext in extensions:
                dest_folder = os.path.join(folder_path, category)
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder,filename)
                shutil.move(file_path, dest_path)
                history.append("moved", dest_path, file_path)
                total_size += os.path.getsize(dest_path)
                break

    print(messages[lang]["done"])
    report(lang, count, total_size, start_time)



# sorting by date (creation / modification)
def organize_by_date(folder_path, lang):
    start_time = datetime.now()
    total_size = 0
    count = 0
    print(messages[lang]["organizing"])

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for filename in tqdm(files, desc="Processing", ncols=80):
        file_path = os.path.join(folder_path, filename)
        timestamp = os.path.getmtime(file_path)
        date = datetime.fromtimestamp(timestamp)
        year, month = str(date.year), str(date.month).zfill(2)
        dest_folder = os.path.join(folder_path, year, month)
        os.makedirs(dest_folder, exist_ok=True)
        dest_path = os.path.join(dest_folder, filename)
        shutil.move(file_path, dest_path)
        history.append(("moved", dest_path, file_path))
        total_size += os.path.getsize(dest_path)
        count+=1

    print(messages[lang]["done"])
    report(lang, count, total_size, start_time)


# sorting by file size
def organize_by_size(folder_path, lang):
    start_time = datetime.now()
    total_size = 0
    count = 0
    print(messages[lang]["organizing"])
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for filename in tqdm(files, desc="Processing", ncols=80):
        file_path = os.path.join(folder_path, filename)
        size = os.path.getsize(file_path) / (1024 * 1024) # convert to MB
        if size < 10:
            size_folder = "Small_Files"
        elif size < 100 :
            size_folder = "Medium_Files"
        else:
            size_folder = "Large_Files"
            
        dest_folder = os.path.join(folder_path, size_folder)
        os.makedirs(dest_folder, exist_ok=True)
        dest_path = os.path.join(dest_folder, filename)
        shutil.move(file_path, dest_path)
        history.append(("moved", dest_path, file_path))
        total_size += os.path.getsize(dest_path)
        count += 1

    print(messages[lang]["done"])
    report(lang, count, total_size,start_time)

def undo_last_action(lang):
    if not history : 
        print(messages[lang]["no_undo"])
        return
    
    action, dest, src = history.pop()
    if action == "moved" and os.path.exists(dest):
        shutil.move(dest, src)
        print(messages[lang]["undo_done"])


def report(lang, count, total_size, start_time)
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    print(messages[lang]["report"].format(files=count, size=total_size / (1024 * 1024), time=elapsed))

def main():
    #choose language
    lang = input(messages["en"]["select_lang"]).strip().lower()
    if lang not in ["fa", "en"]:
        lang = "en"

    print(messages[lang]["welcome"])

    # input path
    folder_path = input(messages[lang]["path_input"]).strip()
    if not os.path.exists(folder_path):
        print(messages[lang]["invalid_path"])
        return

    #choose sorting type
    sort_choice = input(messages[lang]["choose_sort"]).strip()

    #choose categories 
    if sort_choice == "1":
        use_default = input(messages[lang]["use_default"]).strip().lower()
        if use_default == "y":
            categories = default_categories
        else:
            categories = {}
            while True:
                custom = input(messages[lang]["custom_prompt"]).strip()
                if not custom:
                    break
                parts = custom.split()

                if len(parts) == 2:
                    folder_name = parts[0]
                    exts = parts[1].split(",")
                    categories[folder_name] = exts
    
        organize_by_type(folder_path,categories, lang)

    elif sort_choice == "2":
        organize_by_date(folder_path, lang)

    elif sort_choice == "3":
        organize_by_size(folder_path, lang)
    
    else:
        print("❌ invalid choice!")
    
    undo_choice = input(messages[lang]["undo_prompt"]).strip().lower()
    if undo_choice == "y":
        undo_last_action(lang)

if __name__ == "__main__":
    main()
