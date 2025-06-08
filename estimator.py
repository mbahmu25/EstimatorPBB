from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterEnum,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext,
    QgsProcessingOutputLayerDefinition,
    QgsVectorLayer,
    QgsProject,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber
)
from qgis.utils import iface
import geopandas as gpd
import tempfile
import os
import json
import random

# from .report import get_report



class GeoPandasSpatialJoin(QgsProcessingAlgorithm):
    PBT = 'Bidang Tanah'
    BG = "Bangunan"
    ZNT = 'Zona Nilai Tanah'
    ADM = 'Batas Administrasi dan PBB'
    DAERAH = 'Daerah'
    PBBExist = 'PBB Eksisting'
    NJOP_BG = 'NJOP_BG'
    PREDICATE = 'PREDICATE'
    OUTPUT = 'OUTPUT'
    REPORT = 'REPORT'
    TARIF = "Tarif"
    HAK = "HAK"

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GeoPandasSpatialJoin()

    def name(self):
        return 'PBB Estimator'

    def displayName(self):
        return self.tr('PBB Estimator')

    def group(self):
        return self.tr('Pelatihan BPN')

    def groupId(self):
        return 'pbb_estimator'

    def shortHelpString(self):
        return self.tr('Tools untuk membantu analisis PBB')

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.ADM, self.tr('Batas Administrasi dan PBB')))
        self.addParameter(
            QgsProcessingParameterField(
                'DAERAH',  # Gunakan nama unik untuk parameter field
                self.tr('Kolom Nama Daerah'),
                parentLayerParameterName=self.ADM  # Ini referensi ke input layer
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                'PBBExist',  # Gunakan nama unik untuk parameter field
                self.tr('PBB Eksisting'),
                parentLayerParameterName=self.ADM  # Ini referensi ke input layer
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                'TARIF_DAERAH',  # Gunakan nama unik untuk parameter field
                self.tr('Tarif'),
                parentLayerParameterName=self.ADM  # Ini referensi ke input layer
            )
        )
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.PBT, self.tr('Bidang Tanah')))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.BG, self.tr('Bangunan')))
        self.addParameter(QgsProcessingParameterNumber('NJOP_BG',self.tr('Nilai Pajak Bangunan'), type=QgsProcessingParameterNumber.Double, defaultValue=0.1))
        self.addParameter(
            QgsProcessingParameterField(
                'BUILDING_LEVEL_FIELD',  # Gunakan nama unik untuk parameter field
                self.tr('Building Level [optional]'),
                parentLayerParameterName=self.BG,  # Ini referensi ke input layer
                optional = True
            )
        )
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.ZNT, self.tr('Zona Nilai Tanah')))
        
        self.addParameter(
            QgsProcessingParameterField(
                'FIELD_ZNT',  # Gunakan nama unik untuk parameter field
                self.tr('Pilih Field Nilai Tanah'),
                parentLayerParameterName=self.ZNT  # Ini referensi ke input layer
            )
        )
        
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT, self.tr('Output file'), fileFilter='ESRI Shapefile (*.shp)'))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.REPORT, self.tr('Report Output file'), fileFilter='HTML (*.html)'))
    def processAlgorithm(self, parameters, context, feedback):
        admin_layer = self.parameterAsVectorLayer(parameters, self.ADM, context)
        input_layer = self.parameterAsVectorLayer(parameters, self.PBT, context)
        join_layer = self.parameterAsVectorLayer(parameters, self.ZNT, context)
        bg_layer = self.parameterAsVectorLayer(parameters,self.BG,context)
        field_adm = self.parameterAsString(parameters, 'DAERAH', context)
        field_PBBExist = self.parameterAsString(parameters, 'PBBExist', context)
        field_tarif = self.parameterAsString(parameters, 'TARIF_DAERAH', context)
        field_name = self.parameterAsString(parameters, 'FIELD_ZNT', context)
        field_building_level = self.parameterAsDouble(parameters,'BUILDING_LEVEL',context)
        nilai_bg = self.parameterAsDouble(parameters, 'NJOP_BG', context)
        output_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        report_output_path = self.parameterAsFileOutput(parameters, self.REPORT, context)

        if input_layer is None or join_layer is None:
            raise QgsProcessingException("Invalid input or join layer.")

        # Export both layers to temp files
        tmp_dir = tempfile.mkdtemp()
        tmpAdm = os.path.join(tmp_dir, 'admn.gpkg')
        tmp1 = os.path.join(tmp_dir, 'input1.gpkg')
        tmp2 = os.path.join(tmp_dir, 'input2.gpkg')
        tmp3 = os.path.join(tmp_dir, 'input3.gpkg')
        _ = QgsVectorFileWriter.writeAsVectorFormat(
            admin_layer, tmpAdm, "utf-8", input_layer.crs(), "GPKG"
        )
        _ = QgsVectorFileWriter.writeAsVectorFormat(
            input_layer, tmp1, "utf-8", input_layer.crs(), "GPKG"
        )
        _ = QgsVectorFileWriter.writeAsVectorFormat(
            join_layer, tmp2, "utf-8", join_layer.crs(), "GPKG"
        )
        _ = QgsVectorFileWriter.writeAsVectorFormat(
            bg_layer, tmp3, "utf-8", join_layer.crs(), "GPKG"
        )

        # Load with GeoPandas
        pbt = gpd.read_file(tmp1)
        znt = gpd.read_file(tmp2)
        bg = gpd.read_file(tmp3)
        admin = gpd.read_file(tmpAdm)
        znt = znt.to_crs(pbt.crs)
        bg = bg.to_crs(pbt.crs)
        admin = admin.to_crs(pbt.crs)

        # Clip manual dengan overlay
        admin_mask = admin[['geometry']]  # cukup geometri saja

        # Clip PBT, ZNT, dan BG dengan overlay
        pbt = gpd.overlay(pbt, admin_mask, how='intersection')
        znt = gpd.overlay(znt, admin_mask, how='intersection')
        bg = gpd.overlay(bg, admin_mask, how='intersection')


        pbt = pbt.reset_index(drop=True)
        pbt['id_bidang_internal'] = pbt.index

        # Merge Batas Admin dengan PBT
        pbt_adm = gpd.overlay(pbt, admin[['geometry', field_adm, field_tarif, field_PBBExist]], how='intersection')

        # Ambil admin dengan luas terbesar (dominasi)
        pbt_adm['luas'] = pbt_adm.geometry.area
        pbt_adm = pbt_adm.sort_values('luas', ascending=False).drop_duplicates('id_bidang_internal')

        # Merge hasil ke bidang tanah
        pbt = pbt.merge(pbt_adm[['id_bidang_internal', field_adm, field_tarif, field_PBBExist]], on='id_bidang_internal', how='left')

        # Perhitungan ZNT per Bidang Tanah
        pbt_znt = gpd.overlay(pbt, znt[['geometry', field_name]], how='intersection')
        pbt_znt_aggregate = pbt_znt.groupby('id_bidang_internal').agg({field_name: 'sum'}).reset_index()
        pbt = pbt.merge(pbt_znt_aggregate, on='id_bidang_internal', how='left')
        
        # Perhitungan Luas Persil (OPTIONAL jika belum ada data tapi amannya begini aja daripada ambil pusing)
        pbt['luas_persil'] = pbt.geometry.area

        # Perhitungan luas bangunan
        pbt_bg_luas = gpd.overlay(bg, pbt, how='intersection')
        pbt_bg_luas['luas_bangunan'] = pbt_bg_luas.geometry.area
        pbt_aggregate = pbt_bg_luas.groupby('id_bidang_internal').agg({'luas_bangunan': 'sum'}).reset_index()
        
        # Penggabungan ke Bidang Tanah
        pbt_final = pbt.merge(pbt_aggregate, on="id_bidang_internal", how='left')
        pbt_final['luas_bangunan'] = pbt_final['luas_bangunan'].fillna(0)

        # # Drop spatial index columns
        pbt_final = pbt_final.drop(columns=[col for col in pbt_final.columns if col.startswith('index_')], errors='ignore')
        mean_value = pbt_final[field_name].mean(skipna=True)
        pbt_final[field_name] = pbt_final[field_name].fillna(mean_value)

        # Perhitungan PBB
        if field_building_level:
            pbt_final['pajak_bangunan'] = pbt_final[field_building_level].fillna(1)*pbt_final['luas_bangunan']*nilai_bg 
        else:
            pbt_final['pajak_bangunan'] = pbt_final['luas_bangunan']*nilai_bg

        pbt_final['pajak_bumi'] = pbt_final['luas_persil']*pbt_final[field_name] # Asumsi setara masih bisa diganti berdasarkan data
        pbt_final['PBB'] = pbt_final[field_tarif]*(pbt_final['pajak_bangunan']+pbt_final['pajak_bumi'])
        # Save to output
        pbt_final.to_file(output_path, driver='ESRI Shapefile')

        
        layer = QgsVectorLayer(output_path, "Bidang_tanah_dengan_ZNT", "ogr")
        if not layer.isValid():
            raise QgsProcessingException("Output layer is not valid.")
        QgsProject.instance().addMapLayer(layer)
        outputData = dict()
        outputData["luas_area"] = sum(pbt_final.geometry.area)
        outputData["total_bangunan"] = len(bg)
        outputData["total_bidang"] = len(pbt)
        outputData["pajak_bangunan"] = sum(pbt_final['pajak_bangunan'])
        outputData["pajak_bumi"] = sum(pbt_final['pajak_bumi'])
        outputData["total_pbb_eksisting"] = sum(pbt_final[field_PBBExist])
        outputData["total_pbb"] = sum(pbt_final['pajak_bangunan'])+sum(pbt_final['pajak_bumi'])
        outputData["tabel"]=[]
        
        pbb_per_daerah = pbt_final.groupby(field_adm)[[field_PBBExist,"PBB"]].sum().reset_index().rename(columns={field_adm: 'daerah', field_PBBExist: 'pbb_eksisting', "PBB":"pbb_estimasi"}).to_dict(orient="records")

        labels = [d['daerah'] for d in pbb_per_daerah]
        values = [d['pbb_eksisting'] for d in pbb_per_daerah]
        values2 = [d['pbb_estimasi'] for d in pbb_per_daerah]
        colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in pbb_per_daerah]
        colors2 = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in pbb_per_daerah]

        # Buat nested dataset: misalnya 1 level (parent), 1 level (child)
        chart_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "PBB Eksisting Daerah",
                    "data": values,
                    "backgroundColor": colors
                },
                {
                    "label": "PBB Estimasi Daerah",
                    "data": values2,
                    "backgroundColor": colors2
                }
            ]
        }

        

        # Output JSON string untuk disisipkan ke HTML
        chart_data_js = json.dumps(chart_data)


        table ="" 
        for i in pbb_per_daerah:
            table+=f'<tr><td>{i["daerah"]}</td><td>Rp {i["pbb_eksisting"]:,}</td><td>Rp {i["pbb_estimasi"]:,}</td><td>{i["pbb_estimasi"]/i["pbb_eksisting"]*100}</td></tr>'

        html_content = """
        <html>
            <head>
                <script src="https://cdn.tailwindcss.com"></script>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
        """+f"""
            <body class="font-sans p-8 text-gray-600 bg-gray-50">
            <div
                class="bg-white mx-auto my-8 px-10 py-12 shadow-md rounded-md print:shadow-none print:rounded-none print:my-0 print:p-0"
                style="width: 794px; min-height: 1123px"
            >
                <h2 class="text-2xl font-semibold text-blue-600 mb-1">Informasi Data</h2>
                <h3 class="text-lg font-semibold text-black mb-1">Bidang Tanah</h3>

                <table class="table-auto border-collapse border-0 mb-6">
                    <tbody>
                        <tr>
                        <td class="pr-3 text-gray-700 text-[16pt] font-normal">Luas Area</td>
                        <td class="px-2">:</td>
                        <td class="text-[16pt] font-normal text-gray-900">
                            {outputData['luas_area']:.2f} m<sup>2</sup>
                        </td>
                        </tr>
                        <tr>
                        <td class="pr-3 text-gray-700 text-[16pt] font-normal">Total Bangunan</td>
                        <td class="px-2">:</td>
                        <td class="text-[16pt] font-normal text-gray-900">{outputData['total_bangunan']}</td>
                        </tr>
                        <tr>
                        <td class="pr-3 text-gray-700 text-[16pt] font-normal">
                            Total Bidang Tanah
                        </td>
                        <td class="px-2">:</td>
                        <td class="text-[16pt] font-normal text-gray-900">{outputData['total_bidang']}</td>
                        </tr>
                        <tr>
                        <td class="pr-3 text-gray-700 text-[16pt] font-normal">
                            Total Pajak Bangunan
                        </td>
                        <td class="px-2">:</td>
                        <td class="text-[16pt] font-normal text-gray-900">Rp {int(outputData['pajak_bangunan']):,}</td>
                        </tr>
                        <tr>
                        <td class="pr-3 text-gray-700 text-[16pt] font-normal">
                            Total Pajak Bumi
                        </td>
                        <td class="px-2">:</td>
                        <td class="text-[16pt] font-normal text-gray-900">Rp {int(outputData['pajak_bumi']):,}</td>
                        </tr>
                        <tr>
                        <td class="pr-3 text-gray-700 text-[16pt] font-normal">Total PBB</td>
                        <td class="px-2">:</td>
                        <td class="text-[16pt] font-normal text-gray-900">Rp {int(outputData['total_pbb']):,}</td>
                        </tr>
                    </tbody>
                </table>
            """+f"""
            <div class="max-h-48 overflow-y-auto border border-gray-300 bg-white p-4 rounded shadow-sm">
                <h3 class="text-lg font-semibold text-black mb-2">Tabel Pajak</h3>
                <table class="w-full border-collapse">
                    <thead>
                    <tr class="bg-gray-200 text-gray-700 text-center text-sm">
                        <th class="border border-gray-300 px-3 py-1">Nama Daerah</th>
                        <th class="border border-gray-300 px-3 py-1">PBB Eksisting</th>
                        <th class="border border-gray-300 px-3 py-1">PBB Estimasi</th>
                        <th class="border border-gray-300 px-3 py-1">Perubahan (%)</th>
                    </tr>
                    </thead>
                    <tbody id="table-body" class="text-gray-600 text-sm">
                    {table}
                    </tbody>
                </table>
            </div>
                <div class="mt-8 max-w-xs mx-auto">
                    <h3 class="text-lg font-semibold text-black mb-3 text-center">
                        Pie Chart Pajak
                    </h3>
                    <canvas id="nestedPieChart" class="mx-auto"></canvas>
                </div>
            </div>
        </body>
        </html>
        """+"""
    <script>

      const ctx = document.getElementById("nestedPieChart").getContext("2d");
      """+f"""
      const chartData = {chart_data}
      """+"""

      new Chart(ctx, {
        type: 'doughnut',
        data: chartData,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "bottom",
              labels: { font: { size: 14 }, color: "#000" },
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return (
                    context.label +
                    ": Rp " +
                    context.parsed.toLocaleString("id-ID")
                  );
                },
              },
            },
          },
        },
      });
    </script>
"""
        with open(report_output_path,"w") as r:
           r.write(html_content)

        return {self.OUTPUT: output_path}


