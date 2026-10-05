# Auto File Organizer

A small cross-platform desktop utility for sorting files into type-based folders.

Auto File Organizer is intended for everyday folders that accumulate mixed files. The user selects a directory and the application groups supported files into categories such as images, video, documents, music, archives, and code.

## Highlights

- Desktop utility with a simple folder-selection workflow.
- Organizes files by type without deleting them.
- Release builds for Windows, macOS, and Linux.
- Automated cross-platform build and release workflow with GitHub Actions.
- Portable releases available from GitHub Releases.

## Releases

The current published release is **v3.0.1**.

| Platform | Download |
| --- | --- |
| Windows | [AutoFileOrganizer-Windows.exe](https://github.com/amintorbat/auto_file_organizer/releases/latest/download/AutoFileOrganizer-Windows.exe) |
| macOS | [AutoFileOrganizer-macOS](https://github.com/amintorbat/auto_file_organizer/releases/latest/download/AutoFileOrganizer-macOS) |
| Linux | [AutoFileOrganizer-Linux](https://github.com/amintorbat/auto_file_organizer/releases/latest/download/AutoFileOrganizer-Linux) |

## Build from source

The project is implemented in Python. Install the dependencies, then run the application locally:

```bash
git clone https://github.com/amintorbat/auto_file_organizer.git
cd auto_file_organizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python auto_file_organizer_gui.py
```

On Windows, activate the virtual environment with `.venv\Scripts\activate`.

## Release workflow

The repository includes a GitHub Actions workflow that builds platform artifacts and prepares them for GitHub Releases. This keeps the release process reproducible across Windows, macOS, and Linux rather than relying on a single development machine.

## Project scope

This is a focused utility rather than a general-purpose file-management system. Its job is deliberately narrow: take a selected folder and make mixed files easier to navigate by grouping recognized file types.

It does not claim to replace a file manager, provide cloud synchronization, or make decisions about file contents.

## فارسی

**Auto File Organizer** یک ابزار دسکتاپ ساده برای مرتب‌سازی فایل‌های یک پوشه بر اساس نوع آن‌هاست.

کاربر یک پوشه را انتخاب می‌کند و برنامه فایل‌های پشتیبانی‌شده را در دسته‌هایی مثل تصویر، ویدیو، اسناد، موسیقی، آرشیو و کد مرتب می‌کند. برنامه برای ویندوز، macOS و لینوکس خروجی دارد و فایل‌ها را حذف نمی‌کند.

نسخه‌های آماده از بخش Releases همین مخزن قابل دریافت هستند.

## Contributing

Bug reports and focused improvement suggestions are welcome through GitHub Issues and pull requests.
