from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from qgis.utils import iface

# === HTML content (customize this part as needed) ===
html_content = """
<html>
<head>
<style>
    body { font-family: Arial, sans-serif; padding: 20px; }
    h1 { color: #2e6c80; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
</style>
</head>
<body>
    <h1>Sample Report</h1>
    <p>This is a custom HTML report shown in a QGIS window.</p>
    <table>
        <tr><th>Field</th><th>Value</th></tr>
        <tr><td>Operation</td><td>Union</td></tr>
        <tr><td>Feature Count</td><td>123</td></tr>
        <tr><td>Total Area</td><td>45678.90</td></tr>
    </table>
</body>
</html>
"""

# === Dialog class ===
class HtmlReportDialog(QDialog):
    def __init__(self, html, parent=None):
        super().__init__(parent)
        self.setWindowTitle("HTML Report")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        self.browser = QTextBrowser()
        self.browser.setHtml(html)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)

        layout.addWidget(self.browser)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

# === Show dialog in QGIS ===
dialog = HtmlReportDialog(html_content, parent=iface.mainWindow())
dialog.exec_()
