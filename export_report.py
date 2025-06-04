
def get_report(data = {
                'luas_area': 12345,
                'total_bangunan': 15,
                'total_bidang': 30,
                'pajak_bangunan': 12345678,
                'pajak_bumi': 9876543,
                'total_pbb': 22222222,
                'mean_bumi':0,
                'mean_bangunan':0,
                "mean_pbb":0,
                'tabel':[
                    {
                    "nama_daerah":"Cokro",
                    "pajak_bangunan":0,
                    "pajak_bumi":0,
                    "pbb":0
                    },{
                    "nama_daerah":"Cokro",
                    "pajak_bangunan":0,
                    "pajak_bumi":0,
                    "pbb":0
                    },{
                    "nama_daerah":"Cokro",
                    "pajak_bangunan":0,
                    "pajak_bumi":0,
                    "pbb":0
                    },
                    {
                    "nama_daerah":"Cokro",
                    "pajak_bangunan":0,
                    "pajak_bumi":0,
                    "pbb":0
                    },
                    {
                    "nama_daerah":"Cokro",
                    "pajak_bangunan":0,
                    "pajak_bumi":0,
                    "pbb":0
                    }
                ]
            }):
   
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
            """+f"""
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            </head>
            <body>
                <h2>Informasi Data</h2>
                <h3>Bidang Tanah</h3>
                <table border-collapse: collapse;border: 0px;>
                <tr>
                    <td class="text">Luas Area</td>
                    <td class="text">:</td>
                    <td class="text">{data['luas_area']} m<sup>2</sup></td>
                </tr>
                <tr>
                    <td class="text">Total Bangunan</td>
                    <td class="text">:</td>
                    <td class="text">{data['total_bangunan']}</td>
                </tr>
                <tr>
                    <td class="text">Total Bidang Tanah</td>
                    <td class="text">:</td>
                    <td class="text">{data['total_bidang']}</td>
                </tr>
                <tr>
                    <td class="text">Total Pajak Bangunan</td>
                    <td class="text">:</td>
                    <td class="text">Rp {int(data['pajak_bangunan']):,}</td>
                </tr>
                <tr>
                    <td class="text">Total Pajak Bumi</td>
                    <td class="text">:</td>
                    <td class="text">Rp {int(data['pajak_bumi']):,}</td>
                </tr>
                <tr>
                    <td class="text">Total PBB</td>
                    <td class="text">:</td>
                    <td class="text">Rp {int(data['total_pbb']):,}</td>
                </tr>
                <tr>
                    <td class="text">Rata-rata Pajak Bangunan</td>
                    <td class="text">:</td>
                    <td class="text">Rp {int(data['mean_bangunan'])}</td>
                </tr>
                <tr>
                    <td class="text">Rata-rata Pajak Bumi</td>
                    <td class="text">:</td>
                    <td class="text">Rp {int(data['mean_bumi']):,}</td>
                </tr>
                <tr>
                    <td class="text">Rata-rata PBB</td>
                    <td class="text">:</td>
                    <td class="text">Rp {int(data['mean_pbb']):,}</td>
                </tr>
                </table>

                <div class="scroll-table">
                    <h3>Tabel Pajak</h3>
                """+"""
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
                """+f"""
                    <table>
                        <thead>
                            <tr>
                                <th>Nama Daerah</th>
                                <th>Pajak Bangunan</th>
                                <th>Pajak Bumi</th>
                                <th>PBB</th>
                            </tr>
                        </thead>
                        <tbody>
                    """
    for i in data["tabel"]:
        html_content+=f'<tr><td>{i["nama_daerah"]}</td><td>Rp {i["pajak_bangunan"]:,}</td><td>Rp {i["pajak_bumi"]:,}</td><td>Rp {i["pbb"]:,}</td></tr>'
    html_content += f"""
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    with open("report.html","w") as r:
        r.write(html_content)
# get_report()