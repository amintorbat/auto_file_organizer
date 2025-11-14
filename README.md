# Auto File Organizer 🗂️

این برنامه با زبان پایتون ساخته شده و کارش اینه که **فایل‌های شما رو به صورت خودکار داخل پوشه‌های مرتب و منظم قرار بده** 🎯  
یعنی مثلاً اگر داخل یه پوشه عکس، فیلم، آهنگ و فایل متنی قاطی دارین، این برنامه خودش اون‌ها رو جدا می‌کنه و تو پوشه‌های مخصوص خودش می‌ذاره.

## 📋 Requirements (نیازها)

- Python 3.7 or higher (پایتون 3.7 یا بالاتر)
- tqdm library (کتابخانه tqdm)

---

## ✨ ویژگی‌ها

- 🔄 مرتب‌سازی فایل‌ها بر اساس **نوع فایل، تاریخ ایجاد و اندازه**
- ↩️ قابلیت **Undo** برای بازگردانی تغییرات اخیر
- 📊 نمایش **نوار پیشرفت (Progress Bar)** هنگام عملیات
- 🧾 تولید **گزارش عملکرد** در پایان هر اجرا
- ⚙️ ساختار ماژولار و قابل توسعه
- 💡 فقط یک وابستگی ساده (tqdm)

---

## 🧩 دسته‌بندی‌های پیش‌فرض برنامه

| نوع فایل          | پسوندها (Extensions)            |
| ----------------- | ------------------------------- |
| 📷 عکس‌ها         | jpg, jpeg, png, gif, bmp        |
| 🎬 ویدیوها        | mp4, mkv, mov, avi              |
| 📄 اسناد          | pdf, docx, txt, xlsx            |
| 🎵 صداها          | mp3, wav, ogg                   |
| 🗜️ فایل‌های فشرده | zip, rar, 7z                    |
| 💻 کدها           | py, js, html, css, cpp, c, java |

---

## 🪶 آموزش استفاده گام‌به‌گام

حتی اگه تا حالا با کامپیوتر یا پایتون کار نکردی، نگران نباش 💪  
فقط این چند قدم ساده رو دنبال کن 👇

---

### 🔹 مرحله ۱: دریافت برنامه

اول باید برنامه رو دانلود کنی.  
اگر گیت‌هاب داری، با دستور زیر:

```bash
git clone https://github.com/amintorbat/auto_file_organizer.git
```

اگر نداری، خیلی راحت از بالای صفحه‌ی گیت‌هاب روی دکمه‌ی **Code → Download ZIP** بزن و فایل رو دانلود و از حالت فشرده خارج کن.

---

### 🔹 مرحله ۲: نصب وابستگی‌ها (Dependencies)

قبل از اجرای برنامه، باید کتابخانه‌های مورد نیاز رو نصب کنی. این کار خیلی ساده است! 👇

**روش ۱: استفاده از pip (پیشنهادی)**

```bash
pip install -r requirements.txt
```

یا اگر با خطا مواجه شدی:

```bash
python3 -m pip install -r requirements.txt
```

**روش ۲: نصب دستی**

```bash
pip install tqdm==4.67.1
```

---

### 🔹 مرحله ۳: اجرای برنامه

داخل پوشه‌ی برنامه، روی فایل زیر راست‌کلیک کن و بازش کن:

```
file_organizer.py
```

اگر با خط فرمان (ترمینال) کار می‌کنی:

```bash
python file_organizer.py
```

یا:

```bash
python3 file_organizer.py
```

---

### 🔹 مرحله ۴: انتخاب زبان

اول ازت می‌پرسه که زبان برنامه چی باشه 👇
بنویس:

```
fa
```

تا فارسی بشه، یا `en` برای انگلیسی.

---

### 🔹 مرحله ۵: انتخاب مسیر پوشه

بعد ازت می‌پرسه:

```
آدرس پوشه‌ای که می‌خواهید مرتب شود را وارد کنید:
```

کافیه آدرس پوشه‌ای رو بنویسی که می‌خوای فایل‌هاش مرتب بشن.
مثلاً:

```
C:\Users\Amin\Desktop\MyFiles
```

یا در مک:

```
/Users/amin/Desktop/MyFiles
```

---

### 🔹 مرحله ۶: انتخاب نوع دسته‌بندی

برنامه ازت می‌پرسه:

```
آیا می‌خواهید از دسته‌بندی پیش‌فرض استفاده کنید؟ (y/n)
```

اگر تایپ کنی:

- `y` یعنی بله، از دسته‌بندی آماده خودش استفاده کنه.
- `n` یعنی می‌خوای خودت پوشه‌ها و نوع فایل‌ها رو مشخص کنی.

---

### 🔹 مرحله ۷: تمام 🎉

وقتی برنامه کارش رو تموم کنه، می‌نویسه:

```
مرتب‌سازی با موفقیت انجام شد ✅
```

و داخل پوشه‌ات، همه‌چیز منظم و تمیز تو پوشه‌های جدا افتاده 👇
📁 `Images/`
📁 `Videos/`
📁 `Documents/`
📁 `Code/`
و غیره...

---

## 💡 مثال از نتیجه نهایی

قبل از اجرای برنامه 👇

```
MyFiles/
 ├── photo1.jpg
 ├── song.mp3
 ├── report.pdf
 ├── video.mp4
 ├── script.py
```

بعد از اجرای برنامه 👇

```
MyFiles/
 ├── Images/
 │    └── photo1.jpg
 ├── Audio/
 │    └── song.mp3
 ├── Documents/
 │    └── report.pdf
 ├── Videos/
 │    └── video.mp4
 ├── Code/
 │    └── script.py
```

---

## 🚀 Building Releases with GitHub Actions

This project uses GitHub Actions to automatically build executables for Windows, macOS, and Linux when you push a version tag.

### How It Works

1. **Trigger**: The workflow runs automatically when you push a tag starting with `v*` (e.g., `v1.0.0`, `v2.1.3`)

2. **Build Process**: 
   - Three parallel jobs build the app for each platform:
     - `build-windows`: Creates `AutoFileOrganizer.exe` on Windows
     - `build-macos`: Creates `AutoFileOrganizer` binary on macOS
     - `build-linux`: Creates `AutoFileOrganizer` binary on Linux

3. **Release Creation**: After all builds complete, a GitHub Release is automatically created with all three executables attached.

### How to Create a Release

1. **Create and push a version tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically**:
   - Build executables for all three platforms
   - Create a GitHub Release
   - Attach all executables to the release

3. **Download the release** from the GitHub Releases page.

### Workflow File Location

The workflow file is located at: `.github/workflows/build.yml`

### What Gets Built

- **Windows**: `AutoFileOrganizer.exe` (single executable file)
- **macOS**: `AutoFileOrganizer` (single executable file)
- **Linux**: `AutoFileOrganizer` (single executable file)

All executables are built using PyInstaller with the `--windowed` flag (no console window) and `--onefile` (single file output).

---

## 🧾 نسخه فعلی

**نسخه 2.0.0**

## 🧑‍💻 سازنده

**امین تربت اصفهانی**
🔗 [صفحه گیت‌هاب](https://github.com/amintorbat)
💬 اگر خوشت اومد، حتماً ستاره ⭐ بده که پروژه رشد کنه :)

👨‍💻 ساخته‌شده با عشق
