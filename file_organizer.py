
import os
import shutil
from pathlib import Path

# -- languages --
messages = {
    "fa" : {
        "select_lang": "زبان را انتخاب کنید(fa/en):",
        "welcome": "خوش آمدید به برنامه",
        "path_input" : "آدرس پوشه ای را که میخواهید مرتب شود را وارد کنید :",
        "use_default" : "آیا میخواهید از دسته بندی پیش فرض استفاده کنید؟ (y/n):",
        "customm_prompt" :"نام پوشه و پسوند مربوطه را  وارد کنید(مثلا : عکسjpg,png): ",
        "done": "مرتب سازی با موفقیت انجام شد ✅",
        "invalid_path": "آدرس وارد شده معتبر نیست ❌",
        "organizing" : "در حال مرتبسازی فایل ها...",
    },
    "en" : {
        "select_lang" : "Select language (fa/en)",
        "welcome" : "Welcome to Auto File Organizer ",
        "path_input" : "Enter the folder path to organize: ",
        "use_default" : "Do you want to use the default categories? (y/n)",
        "custom_prompt" : "Enter folder name and extensions (e.d., Images jpg,png): ",
        "done": "File organized successfully ✅",
        "invalid_path" : "Invalid folder path ❌",
        "organizing": "Organizing files...",
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

def organize_files(folder_path, categories, lang):
    print(messages[lang]["organizing"])

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.is_file():
            ext = filename.split(".")[-1].lower()
            for category, extensions in categories.items():
                if ext in extensions:
                    dest_folder = os.path.join(folder_path, category)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest_folder,filename))
                    break

    print(messages[lang]["done"])

def main():
    #choose language
    lang = input(messages["en"]["select_lang"]).strip.lower()
    if lang not in ["fa", "en"]:
        lang = "en"

    print(messages[lang]["welcome"])

    # input path
    folder_path = input(messages[lang]["paht_input"]).strip()

    if not os.path.exists(folder_path):
        print(messages[lang]["invalid_path"])
        return

    #choose categories 
    use_default = input(messages[lang]["use_default"]).strip.lower()
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
    
    organize_files(folder_path,categories, lang)

if __name__ == "__main__":
    main()
