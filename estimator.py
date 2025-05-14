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
    QgsProcessingParameterField
)
import geopandas as gpd
import tempfile
import os


class GeoPandasSpatialJoin(QgsProcessingAlgorithm):
    PBT = 'Bidang Tanah'
    BG = "Bangunan"
    ZNT = 'Zona Nilai Tanah'
    PREDICATE = 'PREDICATE'
    OUTPUT = 'OUTPUT'

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
            self.PBT, self.tr('Bidang Tanah')))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.BG, self.tr('Bangunan')))
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

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.PBT, context)
        join_layer = self.parameterAsVectorLayer(parameters, self.ZNT, context)
        bg_layer = self.parameterAsVectorLayer(parameters,self.BG,context)
        field_name = self.parameterAsString(parameters, 'FIELD_ZNT', context)
        output_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)

        if input_layer is None or join_layer is None:
            raise QgsProcessingException("Invalid input or join layer.")

        # Export both layers to temp files
        tmp_dir = tempfile.mkdtemp()
        tmp1 = os.path.join(tmp_dir, 'input1.gpkg')
        tmp2 = os.path.join(tmp_dir, 'input2.gpkg')
        tmp3 = os.path.join(tmp_dir, 'input3.gpkg')

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
        znt = znt.to_crs(pbt.crs)
        bg = bg.to_crs(pbt.crs)

        pbt = pbt.reset_index(drop=True)
        pbt['id_bidang_internal'] = pbt.index

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

        # Perhitungan PBB
        pbt_final['pajak_bangunan'] = pbt_final['luas_bangunan']*10000 # Asumsi setara masih bisa diganti berdasarkan data
        pbt_final['pajak_bumi'] = pbt_final['luas_persil']*20000 # Asumsi setara masih bisa diganti berdasarkan data
        pbt_final['PBB'] = pbt_final['pajak_bangunan']+pbt_final['pajak_bumi']
        # Save to output
        pbt_final.to_file(output_path, driver='ESRI Shapefile')

        
        layer = QgsVectorLayer(output_path, "Bidang_tanah_dengan_ZNT", "ogr")
        if not layer.isValid():
            raise QgsProcessingException("Output layer is not valid.")
        QgsProject.instance().addMapLayer(layer)
        
        
        return {self.OUTPUT: output_path}


