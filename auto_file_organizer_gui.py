import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QMessageBox

def organize_files(folder_path):
    extensions = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documents': ['.pdf', '.docx', '.txt', '.pptx', '.xlsx'],
        'Videos': ['.mp4', '.mkv', '.mov', '.avi'],
        'Music': ['.mp3', '.wav', '.ogg'],
        'Archives': ['.zip', '.rar', '.7z', '.tar'],
        'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.java']
    }

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            for folder_name, exts in extensions.items():
                if ext in exts:
                    new_folder = os.path.join(folder_path, folder_name)
                    os.makedirs(new_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(new_folder, filename))
                    break

class FileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Auto File Organizer")
        self.setGeometry(200, 200, 300, 150)

        self.label = QLabel("Select a folder to organize:", self)
        self.button = QPushButton("Select Folder", self)
        self.button.clicked.connect(self.select_folder)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            organize_files(folder_path)
            QMessageBox.information(self, "Done", "Files organized successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())
