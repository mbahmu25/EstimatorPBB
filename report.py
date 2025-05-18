import csv
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QPushButton,
    QHBoxLayout, QTableWidgetItem, QWidget, QSplitter, QGridLayout, QSizePolicy
)
from qgis.PyQt.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MultiPieChartDialog(QDialog):
    def __init__(self, csv_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pelatihan BPN - Multi Pie Chart Data Pajak")
        self.resize(1200, 650)  # Tinggi sudah disesuaikan agar legend bawah muat

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Tabel kiri
        self.table = QTableWidget()
        splitter.addWidget(self.table)

        # Widget kanan untuk pie chart
        self.chart_widget = QWidget()
        splitter.addWidget(self.chart_widget)

        chart_layout = QGridLayout()
        chart_layout.setContentsMargins(20, 20, 20, 20)
        chart_layout.setHorizontalSpacing(20)
        self.chart_widget.setLayout(chart_layout)

        self.figures = []
        self.canvases = []
        self.axes = []
        for i in range(3):
            fig = Figure(figsize=(4, 4))
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            ax = fig.add_subplot(111)
            self.figures.append(fig)
            self.canvases.append(canvas)
            self.axes.append(ax)
            chart_layout.addWidget(canvas, 0, i)

        # Atur ukuran splitter agar tabel lebih kecil dan pie chart lebih besar
        splitter.setSizes([400, 800])  # Ubah ukuran untuk tabel dan chart
        splitter.setStretchFactor(0, 1)  # Tabel stretch factor kecil
        splitter.setStretchFactor(1, 3)  # Pie chart stretch factor besar

        # Tombol Close di bawah
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)
        main_layout.addLayout(btn_layout)

        self.load_csv_to_table(csv_path)

    def load_csv_to_table(self, filepath):
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return

        if not data:
            print("CSV kosong atau tidak ada data")
            return

        headers = data[0]
        rows = data[1:]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        pajak_bangunan = {}
        pajak_bumi = {}
        pbb = {}

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell))

            try:
                wilayah = row_data[0]
                bangunan = float(row_data[1].replace(',', ''))
                bumi = float(row_data[2].replace(',', ''))
                pbb_val = float(row_data[3].replace(',', ''))
            except Exception:
                bangunan = bumi = pbb_val = 0

            pajak_bangunan[wilayah] = bangunan
            pajak_bumi[wilayah] = bumi
            pbb[wilayah] = pbb_val

        self.plot_pie_chart(pajak_bangunan, 0, "Total Pajak Bangunan")
        self.plot_pie_chart(pajak_bumi, 1, "Total Pajak Bumi")
        self.plot_pie_chart(pbb, 2, "Total PBB")

    def plot_pie_chart(self, data_dict, index, title):
        ax = self.axes[index]
        fig = self.figures[index]
        ax.clear()

        labels = list(data_dict.keys())
        sizes = list(data_dict.values())

        if all(v == 0 for v in sizes):
            ax.text(0.5, 0.5, "No data for chart", ha='center', va='center')
        else:
            wedges, texts, autotexts = ax.pie(
                sizes,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.75,
                wedgeprops=dict(width=0.5),
                textprops={'fontsize': 8}
            )
            ax.legend(
                wedges,
                labels,
                title="Wilayah",
                loc='upper center',
                bbox_to_anchor=(0.5, -0.1),
                fontsize=8,
                ncol=2
            )

        ax.axis('equal')
        ax.set_title(title, pad=20)

        # Beri ruang bawah untuk legend
        fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

        self.canvases[index].draw()

# Ganti path csv dengan path file csv kamu
csv_file_path = r"D:\Downloads\coba1.csv"

dlg = MultiPieChartDialog(csv_file_path)
dlg.exec_()
