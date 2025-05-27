from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from qgis.utils import iface

class HtmlReportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informasi Data Bidang Tanah")
        self.setMinimumSize(700, 900)

        html_content = """
        <html>
        <head>
        <style>
            body { font-family: Arial, sans-serif; padding: 15px; }
            h2 { color: #0066cc; margin-bottom: 5px; }
            h3 { margin-top: 0; }
            p { margin: 2px 0; font-size: 14px; color: #333; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
            th, td { border: 1px solid #ccc; padding: 6px; text-align: center; }
            th { background-color: #f0f0f0; }
            .scroll-table {
                max-height: 120px;
                overflow-y: auto;
                border: 1px solid #ccc;
                margin-top: 10px;
            }
            .diagram-section {
                margin-top: 25px;
            }
            .diagram-title {
                font-weight: bold;
                margin-top: 15px;
                margin-bottom: 5px;
                font-size: 15px;
            }
            .pie-chart {
                width: 280px;
                height: 280px;
                margin-bottom: 20px;
            }
        </style>
        </head>
        <body>
            <h2>Informasi Data</h2>
            <h3>Bidang Tanah</h3>
            <p><b>Luas Area</b></p>
            <p>Total Bangunan</p>
            <p>Total Bidang Tanah</p>
            <p>Total Pajak Bangunan</p>
            <p>Total Pajak Bumi</p>
            <p>Total PBB</p>
            <p>Rata-rata Pajak Bangunan</p>
            <p>Rata-rata Pajak Bumi</p>
            <p>Rata-rata PBB</p>

            <div class="scroll-table">
                <table>
                    <thead>
                        <tr><th>Desa</th><th>Pajak Bangunan</th><th>Pajak Bumi</th><th>PBB</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Kelurahan 1</td><td></td><td></td><td></td></tr>
                        <tr><td>Kelurahan 2</td><td></td><td></td><td></td></tr>
                        <tr><td>Kelurahan 3</td><td></td><td></td><td></td></tr>
                        <tr><td>Kelurahan 4</td><td></td><td></td><td></td></tr>
                    </tbody>
                </table>
            </div>

            <div class="diagram-section">
                <div class="diagram-title">Diagram Pajak</div>

                <div>
                    <div class="diagram-title">Pajak Bangunan</div>
                    <!-- Placeholder pie chart (replace with actual images or SVG) -->
                    <svg class="pie-chart" viewBox="0 0 32 32" width="280" height="280">
                        <circle r="16" cx="16" cy="16" fill="#f0f0f0"/>
                        <circle r="16" cx="16" cy="16" fill="#4caf50" stroke="#fff" stroke-width="0.5" stroke-dasharray="50 50" transform="rotate(-90 16 16)" />
                        <circle r="16" cx="16" cy="16" fill="#2196f3" stroke="#fff" stroke-width="0.5" stroke-dasharray="25 75" transform="rotate(-40 16 16)" />
                    </svg>
                </div>

                <div>
                    <div class="diagram-title">Pajak Bumi</div>
                    <svg class="pie-chart" viewBox="0 0 32 32" width="280" height="280">
                        <circle r="16" cx="16" cy="16" fill="#f0f0f0"/>
                        <circle r="16" cx="16" cy="16" fill="#ff9800" stroke="#fff" stroke-width="0.5" stroke-dasharray="60 40" transform="rotate(-90 16 16)" />
                        <circle r="16" cx="16" cy="16" fill="#9c27b0" stroke="#fff" stroke-width="0.5" stroke-dasharray="30 70" transform="rotate(-50 16 16)" />
                    </svg>
                </div>

                <div>
                    <div class="diagram-title">PBB</div>
                    <svg class="pie-chart" viewBox="0 0 32 32" width="280" height="280">
                        <circle r="16" cx="16" cy="16" fill="#f0f0f0"/>
                        <circle r="16" cx="16" cy="16" fill="#e91e63" stroke="#fff" stroke-width="0.5" stroke-dasharray="70 30" transform="rotate(-90 16 16)" />
                        <circle r="16" cx="16" cy="16" fill="#00bcd4" stroke="#fff" stroke-width="0.5" stroke-dasharray="20 80" transform="rotate(-60 16 16)" />
                    </svg>
                </div>
            </div>
        </body>
        </html>
        """

        layout = QVBoxLayout()

        self.browser = QTextBrowser()
        self.browser.setHtml(html_content)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)

        layout.addWidget(self.browser)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

# Tampilkan dialog di QGIS
dialog = HtmlReportDialog(parent=iface.mainWindow())
dialog.exec_()
