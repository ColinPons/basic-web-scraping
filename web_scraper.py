import requests, csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import List, Tuple
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton,\
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QAbstractItemView, QFileDialog

def scrape_tags(url: str) -> List[Tuple[str, str]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tags = []
    for tag in soup.find_all(True):
        if tag.string:
            tags.append((tag.name, tag.string.strip()))

    return tags

def format_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or parsed.path

    if not netloc.startswith("www."):
        netloc = "www." + netloc

    return scheme + "://" + netloc

class ScraperApp(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.url_input = QLineEdit(self)
        self.fetch_button = QPushButton("Fetch tags", self)
        self.tag_list = QListWidget(self)

        self.fetch_button.clicked.connect(self.fetch_tags)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.tag_list)

        # Add functionality to export to csv
        self.tag_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.clicked.connect(self.export_to_csv)

        layout.addWidget(self.export_button)


    def fetch_tags(self) -> None:
        url = self.url_input.text()

        formatted_url = format_url(url=url)
        self.url_input.setText(formatted_url)
        tags = scrape_tags(formatted_url)

        for tag in tags:
            if tag[1] is not None:
                item = QListWidgetItem(f'{tag[0]}: {tag[1]}')
                self.tag_list.addItem(item)

    def export_to_csv(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for item in self.tag_list.selectedItems():
                    writer.writerow([item.text()])

def main() -> None:

    app = QApplication([])
    window = ScraperApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()