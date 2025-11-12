# auto_file_organizer_gui.py
import sys
import os
import shutil
import time
from datetime import datetime

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QComboBox, QProgressBar, QTextEdit
)

# --- import constants & undo/history from your CLI module ---
# Make sure file_organizer.py is in the same folder
from file_organizer import default_categories, messages, history, undo_last_action

# Worker thread that performs the sorting and emits progress and final report
class OrganizerWorker(QThread):
    progress_changed = pyqtSignal(int)     # percentage 0-100
    status_changed = pyqtSignal(str)       # short status text
    finished_signal = pyqtSignal(dict)     # final stats dict or error

    def __init__(self, folder_path: str, method: str, lang: str):
        super().__init__()
        self.folder_path = folder_path
        self.method = method  # "type" | "date" | "size"
        self.lang = lang
        self._is_cancelled = False

    def run(self):
        start_time = datetime.now()
        try:
            # collect file list (only files, skip dirs)
            files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
            total_files = len(files)
            moved_count = 0
            total_moved_bytes = 0

            if total_files == 0:
                # nothing to do
                self.progress_changed.emit(100)
                report = {
                    "ok": True,
                    "files": 0,
                    "size_bytes": 0,
                    "time_sec": 0.0,
                    "path": self.folder_path,
                    "method": self.method,
                }
                self.finished_signal.emit(report)
                return

            for idx, filename in enumerate(files):
                if self._is_cancelled:
                    # emit what we have so far as cancelled
                    break

                file_path = os.path.join(self.folder_path, filename)
                # safety: skip if file moved by other process
                if not os.path.exists(file_path) or not os.path.isfile(file_path):
                    # update progress and continue
                    self.status_changed.emit(f"{filename} - skipped")
                    percent = int(((idx + 1) / total_files) * 100)
                    self.progress_changed.emit(percent)
                    continue

                # determine destination based on method
                dest_folder = None
                if self.method == "type":
                    ext = filename.split(".")[-1].lower() if "." in filename else ""
                    found = False
                    for category, exts in default_categories.items():
                        if ext in exts:
                            dest_folder = os.path.join(self.folder_path, category)
                            found = True
                            break
                    if not found:
                        dest_folder = os.path.join(self.folder_path, "Others")
                elif self.method == "date":
                    timestamp = os.path.getmtime(file_path)
                    date = datetime.fromtimestamp(timestamp)
                    year = str(date.year)
                    month = str(date.month).zfill(2)
                    dest_folder = os.path.join(self.folder_path, year, month)
                elif self.method == "size":
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    if size_mb < 10:
                        size_folder = "Small_Files"
                    elif size_mb < 100:
                        size_folder = "Medium_Files"
                    else:
                        size_folder = "Large_Files"
                    dest_folder = os.path.join(self.folder_path, size_folder)
                else:
                    dest_folder = os.path.join(self.folder_path, "Unsorted")

                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, filename)

                # move file
                try:
                    shutil.move(file_path, dest_path)
                    # record history (same format as CLI)
                    history.append(("moved", dest_path, file_path))
                    moved_count += 1
                    # update moved size (size after move)
                    try:
                        total_moved_bytes += os.path.getsize(dest_path)
                    except Exception:
                        pass

                    # update status & progress
                    self.status_changed.emit(f"Moved: {filename}")
                except Exception as e:
                    # skip on error but record status
                    self.status_changed.emit(f"Error: {filename}")
                percent = int(((idx + 1) / total_files) * 100)
                self.progress_changed.emit(percent)

            end_time = datetime.now()
            elapsed = (end_time - start_time).total_seconds()

            report = {
                "ok": True,
                "files": moved_count,
                "size_bytes": total_moved_bytes,
                "time_sec": elapsed,
                "path": self.folder_path,
                "method": self.method,
            }
            self.finished_signal.emit(report)

        except Exception as e:
            # on unexpected failure, emit an error report
            self.finished_signal.emit({"ok": False, "error": str(e)})

    def cancel(self):
        self._is_cancelled = True


# --- Main GUI ---
class FileOrganizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.folder_path = None
        self.worker = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Auto File Organizer")
        self.setGeometry(300, 200, 560, 420)

        layout = QVBoxLayout()

        # language selector
        top_row = QHBoxLayout()
        lang_label = QLabel("Language / زبان:")
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(["English", "فارسی"])
        self.lang_selector.currentIndexChanged.connect(self.on_change_lang)
        top_row.addWidget(lang_label)
        top_row.addWidget(self.lang_selector)
        layout.addLayout(top_row)

        # welcome / path label
        self.status_label = QLabel(messages[self.lang]["welcome"])
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # folder choose
        choose_row = QHBoxLayout()
        self.path_display = QLabel("📁 " + "No folder selected")
        choose_btn = QPushButton("Choose Folder")
        choose_btn.clicked.connect(self.on_choose_folder)
        choose_row.addWidget(self.path_display, 4)
        choose_row.addWidget(choose_btn, 1)
        layout.addLayout(choose_row)

        # sorting selector
        method_row = QHBoxLayout()
        method_label = QLabel("")
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Sort by File Type / نوع فایل",
            "Sort by Date / تاریخ",
            "Sort by Size / اندازه"
        ])
        method_row.addWidget(QLabel("Sorting method:"))
        method_row.addWidget(self.method_combo)
        layout.addLayout(method_row)

        # buttons: start, undo, cancel
        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("Start Organizing")
        self.start_btn.clicked.connect(self.on_start)
        self.undo_btn = QPushButton("Undo Last Action")
        self.undo_btn.clicked.connect(self.on_undo)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.on_cancel)
        self.cancel_btn.setEnabled(False)

        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.undo_btn)
        btn_row.addWidget(self.cancel_btn)
        layout.addLayout(btn_row)

        # progress + live status
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.live_status = QLabel("")
        layout.addWidget(self.live_status)

        # report box
        layout.addWidget(QLabel("Report:"))
        self.report_box = QTextEdit()
        self.report_box.setReadOnly(True)
        layout.addWidget(self.report_box)

        self.setLayout(layout)
        self.update_texts()

    def update_texts(self):
        # set UI texts based on language
        if self.lang == "fa":
            self.start_btn.setText("شروع مرتب‌سازی")
            self.undo_btn.setText("بازگردانی آخرین عملیات")
            self.cancel_btn.setText("لغو")
            self.method_combo.setItemText(0, "نوع فایل / Sort by File Type")
            self.method_combo.setItemText(1, "تاریخ / Sort by Date")
            self.method_combo.setItemText(2, "اندازه / Sort by Size")
        else:
            self.start_btn.setText("Start Organizing")
            self.undo_btn.setText("Undo Last Action")
            self.cancel_btn.setText("Cancel")
            self.method_combo.setItemText(0, "Sort by File Type / نوع فایل")
            self.method_combo.setItemText(1, "Sort by Date / تاریخ")
            self.method_combo.setItemText(2, "Sort by Size / اندازه")

    def on_change_lang(self):
        selected = self.lang_selector.currentText()
        self.lang = "fa" if selected == "فارسی" else "en"
        self.status_label.setText(messages[self.lang]["welcome"])
        # update button labels etc
        self.update_texts()

    def on_choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            display = folder if len(folder) < 80 else "..." + folder[-77:]
            self.path_display.setText("📁 " + display)
            self.status_label.setText(messages[self.lang]["path_input"])

    def on_start(self):
        if not self.folder_path or not os.path.exists(self.folder_path):
            QMessageBox.warning(self, "⚠️", messages[self.lang]["invalid_path"])
            return

        # determine method
        idx = self.method_combo.currentIndex()
        method = "type" if idx == 0 else ("date" if idx == 1 else "size")

        # disable UI while running
        self.start_btn.setEnabled(False)
        self.undo_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.report_box.clear()
        self.progress.setValue(0)
        self.live_status.setText(messages[self.lang]["organizing"])

        # create and start worker thread
        self.worker = OrganizerWorker(self.folder_path, method, self.lang)
        self.worker.progress_changed.connect(self.progress.setValue)
        self.worker.status_changed.connect(self.live_status.setText)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_cancel(self):
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.live_status.setText("Cancelled")
            self.cancel_btn.setEnabled(False)

    def on_undo(self):
        # call undo_last_action from file_organizer
        try:
            undo_last_action(self.lang)
            QMessageBox.information(self, "✅", messages[self.lang]["undo_done"])
        except Exception as e:
            QMessageBox.critical(self, "❌", str(e))

    def on_finished(self, report: dict):
        # re-enable UI
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.undo_btn.setEnabled(True)
        self.worker = None

        if not report.get("ok", True):
            # error case
            error = report.get("error", "Unknown error")
            QMessageBox.critical(self, "❌ Error", f"{error}")
            return

        files = report.get("files", 0)
        size_mb = report.get("size_bytes", 0) / (1024 * 1024) if report.get("size_bytes", 0) else 0.0
        time_sec = report.get("time_sec", 0.0)
        path = report.get("path", self.folder_path)
        method = report.get("method", "type")

        # method label per language
        method_label = {
            "type": {"en": "File Type", "fa": "نوع فایل"},
            "date": {"en": "Date", "fa": "تاریخ"},
            "size": {"en": "Size", "fa": "اندازه"},
        }[method][self.lang]

        # longer, friendly report text (localized)
        if self.lang == "fa":
            report_text = (
                f"✅ عملیات با موفقیت انجام شد!\n"
                f"📂 مسیر پوشه: {path}\n"
                f"📊 جزئیات عملکرد:\n"
                f"  • تعداد فایل‌های منتقل‌شده: {files}\n"
                f"  • حجم کل منتقل‌شده: {size_mb:.2f} مگابایت\n"
                f"  • مدت زمان اجرا: {time_sec:.2f} ثانیه\n"
                f"⚙️ روش مرتب‌سازی: {method_label}\n\n"
                "در صورت نیاز می‌توانید با کلیک روی «بازگردانی آخرین عملیات» تغییرات را لغو کنید 🔄"
            )
        else:
            report_text = (
                f"✅ Operation completed successfully!\n"
                f"📂 Folder path: {path}\n"
                f"📊 Summary:\n"
                f"  • Files moved: {files}\n"
                f"  • Total moved: {size_mb:.2f} MB\n"
                f"  • Time taken: {time_sec:.2f} sec\n"
                f"⚙️ Sorting method: {method_label}\n\n"
                "Thank you for using Auto File Organizer 💚\n"
                "If needed, press 'Undo Last Action' to revert the latest changes 🔄"
            )

        # show in UI and message box
        self.report_box.setPlainText(report_text)
        QMessageBox.information(self, "✅", report_text)

# Run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = FileOrganizerGUI()
    gui.show()
    sys.exit(app.exec_())
