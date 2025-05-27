from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qgis.utils import iface

class HtmlReportWebDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informasi Data Bidang Tanah")
        self.resize(360, 640)  # ukuran sesuai yang kamu mau

        layout = QVBoxLayout()

        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

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
        </style>
        </head>
        <body>
            <h2>Informasi Data</h2>
            <h3>Bidang Tanah</h3>
            <table border-collapse: collapse;border: 0px;>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Luas Area</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">12345 m<sup>2</sup></td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Total Bangunan</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">15</td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Total Bidang Tanah</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">30</td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Total Pajak Bangunan</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">Rp 12.345.678</td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Total Pajak Bumi</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">Rp 9.876.543</td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Total PBB</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">Rp 22.222.222</td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Rata-rata Pajak Bangunan</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">Rp 1.234.567</td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Rata-rata Pajak Bumi</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">Rp 987.654</td>
              </tr>
              <tr>
                <td style="padding: 4px; text-align: left; font-weight: normal; color:#ACABAB;">Rata-rata PBB</td>
                <td style="padding: 4px; text-align: center; color:#ACABAB;">:</td>
                <td style="padding: 4px; text-align: left; color:#ACABAB;">Rp 1.111.111</td>
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

            <div class="diagram-section">
                <h3>Diagram Pajak</h3>

                <div>
                    <div class="diagram-title">Pajak Bangunan</div>
                    <svg class="pie-chart" viewBox="0 0 32 32" >
                        <circle r="16" cx="16" cy="16" fill="#f0f0f0"/>
                        <circle r="16" cx="16" cy="16" fill="#4caf50" stroke="#fff" stroke-width="0.5" stroke-dasharray="50 50" transform="rotate(-90 16 16)" />
                        <circle r="16" cx="16" cy="16" fill="#2196f3" stroke="#fff" stroke-width="0.5" stroke-dasharray="25 75" transform="rotate(-40 16 16)" />
                    </svg>
                </div>

                <div>
                    <div class="diagram-title">Pajak Bumi</div>
                    <svg class="pie-chart" viewBox="0 0 32 32" >
                        <circle r="16" cx="16" cy="16" fill="#f0f0f0"/>
                        <circle r="16" cx="16" cy="16" fill="#ff9800" stroke="#fff" stroke-width="0.5" stroke-dasharray="60 40" transform="rotate(-90 16 16)" />
                        <circle r="16" cx="16" cy="16" fill="#9c27b0" stroke="#fff" stroke-width="0.5" stroke-dasharray="30 70" transform="rotate(-50 16 16)" />
                    </svg>
                </div>

                <div>
                    <div class="diagram-title">PBB</div>
                    <svg class="pie-chart" viewBox="0 0 32 32" >
                        <circle r="16" cx="16" cy="16" fill="#f0f0f0"/>
                        <circle r="16" cx="16" cy="16" fill="#e91e63" stroke="#fff" stroke-width="0.5" stroke-dasharray="70 30" transform="rotate(-90 16 16)" />
                        <circle r="16" cx="16" cy="16" fill="#00bcd4" stroke="#fff" stroke-width="0.5" stroke-dasharray="20 80" transform="rotate(-60 16 16)" />
                    </svg>
                </div>
            </div>
        </body>
        </html>
        """

        self.webview.setHtml(html_content)

# Tampilkan dialog di QGIS
dialog = HtmlReportWebDialog(parent=iface.mainWindow())
dialog.exec_()
