from qgis.PyQt.QtWidgets import QAction, QFileDialog, QTableWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QTableWidget, QPushButton, QWidget, QApplication, QSplitter
from qgis.PyQt.QtCore import Qt
from qgis.utils import iface
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class TaxInfoPlugin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tax Info Plugin")
        self.resize(900, 700)

        # Button Import CSV
        self.btnImport = QPushButton("Import CSV")

        # Text Summary
        self.textSummary = QTextBrowser()
        self.textSummary.setMinimumHeight(120)

        # Table Widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setMinimumHeight(200)

        # Layout untuk chart
        self.chartLayout = QHBoxLayout()

        # Layout utama
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.btnImport)
        mainLayout.addWidget(QLabel("Informasi Data"))
        mainLayout.addWidget(self.textSummary)
        mainLayout.addWidget(QLabel("Tabel Data"))
        mainLayout.addWidget(self.tableWidget)
        mainLayout.addWidget(QLabel("Diagram Pajak"))
        mainLayout.addLayout(self.chartLayout)
        self.setLayout(mainLayout)

        # Connect tombol import
        self.btnImport.clicked.connect(self.load_csv)

    def load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Pilih File CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        try:
            self.df = pd.read_csv(path)
        except Exception as e:
            iface.messageBar().pushCritical("Tax Info Plugin", f"Gagal baca CSV: {e}")
            return

        self.show_summary()
        self.show_table()
        self.show_charts()

    def show_summary(self):
        luas_area = self.df.get('Luas Area', pd.Series([0])).sum()
        total_bangunan = self.df.get('Pajak Bangunan', pd.Series([0])).sum()
        total_bumi = self.df.get('Pajak Bumi', pd.Series([0])).sum()
        total_pbb = self.df.get('PBB', pd.Series([0])).sum()

        text = (f"<b>Bidang Tanah</b><br>"
                f"Luas Area: {luas_area}<br>"
                f"Total Pajak Bangunan: {total_bangunan}<br>"
                f"Total Pajak Bumi: {total_bumi}<br>"
                f"Total PBB: {total_pbb}<br>")
        self.textSummary.setHtml(text)

    def show_table(self):
        df = self.df.fillna('')
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(df))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns.tolist())

        for i, row in df.iterrows():
            for j, col in enumerate(df.columns):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row[col])))
        self.tableWidget.resizeColumnsToContents()

    def show_charts(self):
        # Bersihkan layout chart dulu
        while self.chartLayout.count():
            item = self.chartLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Buat 3 pie chart berdasarkan kolom pajak
        self.create_pie_chart('Pajak Bangunan')
        self.create_pie_chart('Pajak Bumi')
        self.create_pie_chart('PBB')

    def create_pie_chart(self, column):
        if column not in self.df.columns:
            return
        data = self.df.groupby('Blok')[column].sum()
        if data.empty:
            return

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
        ax.set_title(column)
        ax.axis('equal')

        canvas = FigureCanvas(fig)
        self.chartLayout.addWidget(canvas)
        canvas.draw()

# Untuk jalankan langsung di QGIS Python Console:
plugin = TaxInfoPlugin()
plugin.show()
