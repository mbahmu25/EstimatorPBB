from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser,
    QWidget, QScrollArea
)
from qgis.utils import iface
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from io import BytesIO
# === HTML content (customize this part as needed) ===


# === Dialog class ===
class HtmlReportDialog(QDialog):
    def __init__(self, parent=None):
        
        isian ="<h1>{a}</h1>"
        a = 100*123125
        isian += f"<h1>{a}</h1>"
        html_content = """
        <html>
        <head>
        
        <style>
            body { font-family: 'Segoe UI', sans-serif; padding: 30px; color: #ACABAB; }
            h2 { color: #0066cc; margin-bottom: 1px; }
            h3 { margin-top: 1px; margin-bottom:1px; color: #000; }
            
            
            .scroll-table {
                max-height: 120px;
                overflow-y: auto;
                border: 1px solid #ccc;
                margin-top: 10px;
                background-color: white;
            }
            .diagram-section {
                margin-top: 25px;
            }
            .diagram-title {
                font-weight: bold;
                margin-top: 15px;
                margin-bottom: 5px;
                font-size: 15px;
                color: #000;
            }
            .pie-chart {
                width: 280px;
                height: 280px;
                margin-bottom: 20px;
            }
            td.text {
                padding: 4px; 
                text-align: left; 
                font-weight: normal; 
                color:#0f0f0f;
                font-size: 8pt;
            }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body>
            <h2>Informasi Data</h2>
            <h3>Bidang Tanah</h3>
            <table border-collapse: collapse;border: 0px;>
              <tr>
                <td class="text">Luas Area</td>
                <td class="text">:</td>
                <td class="text">12345 m<sup>2</sup></td>
              </tr>
              <tr>
                <td class="text">Total Bangunan</td>
                <td class="text">:</td>
                <td class="text">15</td>
              </tr>
              <tr>
                <td class="text">Total Bidang Tanah</td>
                <td class="text">:</td>
                <td class="text">30</td>
              </tr>
              <tr>
                <td class="text">Total Pajak Bangunan</td>
                <td class="text">:</td>
                <td class="text">Rp 12.345.678</td>
              </tr>
              <tr>
                <td class="text">Total Pajak Bumi</td>
                <td class="text">:</td>
                <td class="text">Rp 9.876.543</td>
              </tr>
              <tr>
                <td class="text">Total PBB</td>
                <td class="text">:</td>
                <td class="text">Rp 22.222.222</td>
              </tr>
              <tr>
                <td class="text">Rata-rata Pajak Bangunan</td>
                <td class="text">:</td>
                <td class="text">Rp 1.234.567</td>
              </tr>
              <tr>
                <td class="text">Rata-rata Pajak Bumi</td>
                <td class="text">:</td>
                <td class="text">Rp 987.654</td>
              </tr>
              <tr>
                <td class="text">Rata-rata PBB</td>
                <td class="text">:</td>
                <td class="text">Rp 1.111.111</td>
              </tr>
            </table>

            <div class="scroll-table">
                <h3>Tabel Pajak</h3>
                <style>
                th, td {
                border: 1px solid #ccc; padding: 6px; text-align: center; color: #333;
                background-color: white;
            }
            th {
                background-color: #f0f0f0;
            }
            td.left {
                text-align: left;
                font-weight: normal;
                color: #ACABAB;
            }
            td.center {
                text-align: center;
                color: #ACABAB;
            }
            td.right {
                text-align: right;
                color: #ACABAB;
            }
            </style>
                <table>
                    <thead>
                        <tr>
                            <th>Desa</th>
                            <th>Pajak Bangunan</th>
                            <th>Pajak Bumi</th>
                            <th>PBB</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Kelurahan 1</td><td>Rp 100.000</td><td>Rp 200.000</td><td>Rp 300.000</td></tr>
                        <tr><td>Kelurahan 2</td><td>Rp 110.000</td><td>Rp 210.000</td><td>Rp 310.000</td></tr>
                        <tr><td>Kelurahan 3</td><td>Rp 120.000</td><td>Rp 220.000</td><td>Rp 320.000</td></tr>
                        <tr><td>Kelurahan 4</td><td>Rp 130.000</td><td>Rp 230.000</td><td>Rp 330.000</td></tr>
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        super().__init__(parent)
        self.setWindowTitle("Report PBB Daerah")
        self.setMinimumSize(600, 500)

        # === Scroll Area utama ===
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # === Widget kontainer yang bisa discroll ===
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        
        
        self.browser = QTextBrowser()
        self.browser.setHtml(html_content)
        self.browser.setMinimumHeight(500)

        scroll_layout.addWidget(self.browser)

        # === Masukkan scroll_content ke scroll_area ===
        scroll_area.setWidget(scroll_content)

        # === Layout utama dialog ===
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        # Tombol Close di bawah (tetap terlihat)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        main_layout.addWidget(self.close_button)
        
        # === Chart ===
        self.chart_label = QLabel()
        self.chart_label.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(self.chart_label)

        # Render chart
        self.render_pie_chart()
        
    def render_pie_chart(self):
        # Contoh data pajak
        labels = ['Pajak Bangunan', 'Pajak Bumi', 'Lainnya']
        sizes = [45, 30, 25]
        colors = ['#4caf50', '#ff9800', '#9c27b0']

        fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
        ax.set_title("Diagram Pajak (PBB)")

        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        self.chart_label.setPixmap(pixmap)

        plt.close(fig)
# === Show dialog in QGIS ===
dialog = HtmlReportDialog(parent=iface.mainWindow())
dialog.exec_()
