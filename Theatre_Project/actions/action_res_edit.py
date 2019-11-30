
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from actions.action_res_ajout import AppResAjout

# Classe permettant d'afficher la fonction à compléter 1
class AppResEdit(QDialog):

    res_ajout_dialog = None
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/res_edit.ui", self)
        self.data = data
        self.refreshResult()

    def open_res_ajout(self):
        if self.res_ajout_dialog is not None:
            self.res_ajout_dialog.close()
        self.res_ajout_dialog = AppResAjout(self.data)
        self.res_ajout_dialog.show()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        #display.refreshLabel(self.ui.label_fct_comp_1, "")
        try:
            cursor = self.data.cursor()
            # TODO 1.1 : mettre à jour la requête et changer aussi le fichier ui correspondant
            result = cursor.execute("SELECT noSpec, dateRep, noPlace, noRang, dateEmTick, libelleCat, noDos FROM LesTickets;")
        except Exception as e:
            self.ui.table.setRowCount(0)
            #display.refreshLabel(self.ui.label_fct_comp_1, "Impossible d'afficher les résultats : " + repr(e))
            print("Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table, result)
    def ajout(self):
            self.selected_row = self.ui.table.selectedItems()
            print(self.selected_row[0].text())
