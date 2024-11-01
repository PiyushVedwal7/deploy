import sys
import requests
import webbrowser
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QTextBrowser,
    QWidget,
    QMessageBox,
)
from PyQt5.QtGui import QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from bs4 import BeautifulSoup

# Register the Opera browser
webbrowser.register('opera', None, webbrowser.BackgroundBrowser("C:/Program Files/Opera/launcher.exe"))  # Adjust this path accordingly

class SearchThread(QThread):
    results_ready = pyqtSignal(list)

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def run(self):
        self.results_ready.emit(self.search_yahoo(self.keyword))

    @staticmethod
    def search_yahoo(keyword):
        url = f"https://search.yahoo.com/search?p={keyword}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if "yahoo.com" not in href and not href.startswith("/"):
                        title, summary = SearchThread.fetch_title_and_summary(href)
                        results.append((href, title, summary))
                return results
            else:
                return []
        except requests.RequestException:
            return []

    @staticmethod
    def fetch_title_and_summary(url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                page_soup = BeautifulSoup(response.content, 'html.parser')
                title = page_soup.title.string if page_soup.title else "No Title Available"
                description = page_soup.find("meta", attrs={"name": "description"})
                if description and description.get("content"):
                    summary = description["content"]
                else:
                    paragraph = page_soup.find("p")
                    summary = paragraph.text.strip() if paragraph else "No description available."
                return title, summary
        except requests.RequestException:
            pass
        return "No Title Available", "No description available."

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yahoo Search")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))  # Set your application icon

        font = QFont("Arial", 10)
        self.setFont(font)

        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("Enter keyword to search on Yahoo...")
        self.address_bar.setStyleSheet("padding: 10px; border: 2px solid #0078d7; border-radius: 5px;")
        self.address_bar.setCursor(QCursor(Qt.IBeamCursor))

        self.search_button = QPushButton("Search", self)
        self.search_button.setStyleSheet(""" 
            background-color: #0078d7; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px;
        """)
        self.search_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_button.clicked.connect(self.perform_search)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setStyleSheet(""" 
            background-color: #f44336; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px;
        """)
        self.clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_button.clicked.connect(self.clear_results)

        self.results_area = QTextBrowser(self)
        self.results_area.setOpenExternalLinks(True)
        self.results_area.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        self.results_area.anchorClicked.connect(self.open_link)

        layout = QVBoxLayout()
        layout.addWidget(self.address_bar)
        layout.addWidget(self.search_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.results_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

    def perform_search(self):
        keyword = self.address_bar.text().strip()
        if not keyword:
            QMessageBox.warning(self, "Input Error", "Please enter a keyword to search.")
            return

        self.results_area.clear()
        self.results_area.append(f"<h2>Searching for: <i>{keyword}</i></h2>")
        self.thread = SearchThread(keyword)
        self.thread.results_ready.connect(self.display_results)
        self.thread.start()

    def display_results(self, results):
        if results:
            for result, title, summary in results:
                self.results_area.append(f"""
                    <div style="margin-bottom: 15px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                        <div style="color: #006621; font-size: 12px;">{result}</div>
                        <div style="color: #1a0dab; font-size: 18px; font-weight: bold;">
                            <a href='{result}' style='text-decoration: none;'>{title}</a>
                        </div>
                        <div style="color: #545454; font-size: 14px;">
                            {summary}
                        </div>
                    </div>
                    <hr style="border: 1px solid #e0e0e0;" />
                """)
        else:
            self.results_area.append("No results found or failed to retrieve.")

    def clear_results(self):
        self.address_bar.clear()
        self.results_area.clear()

    def open_link(self, url: QUrl):
        # Open the link in the Opera browser
        webbrowser.get('opera').open(url.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
