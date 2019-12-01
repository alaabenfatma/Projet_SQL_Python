
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppSpectacle(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/spectacles.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_comp_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("WITH nbPlaces AS (SELECT * FROM LesPlaces) SELECT noSpec, nomSpec, dateRep, ((SELECT count(*) FROM nbPlaces) - nbPlacesDispoRep) AS nbPlacesReserves  FROM LesSpectacles NATURAL JOIN LesRepresentations ORDER BY noSpec;")
            display.refreshLabel(self.ui.label_fct_comp_1, "")
        except Exception as e:
            self.ui.table_fct_comp_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_comp_1, result)