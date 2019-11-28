import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from actions.action_add_spec import AppAddSpec
# Classe permettant d'afficher la fonction à compléter 1
class AppEditSpec(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/spec_edit.ui", self)
        self.data = data
        self.spec_ajout = None
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        #display.refreshLabel(self.ui.label_fct_comp_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT * FROM LesSpectacles;")
        except Exception as e:
            self.ui.table.setRowCount(0)
            #display.refreshLabel(self.ui.label_fct_comp_1, "Impossible d'afficher les résultats : " + repr(e))
            print("Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table, result)
    def ajout(self):
            if self.spec_ajout is not None:
                self.spec_ajout.close()
            self.spec_ajout = AppAddSpec(self.data,self)
            self.spec_ajout.show()
    def delete(self):
        self.selected_row = self.ui.table.selectedItems()
        msg =  QMessageBox()
        msg.setWindowTitle("Suppression")
        msg.setText("Voulez-vous vraiment supprimer ce spectacle?")
        msg.setStandardButtons(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        if(msg.exec() == QMessageBox.Yes):
            try:
                 result = self.cursor.execute(
                    "insert into LesSpectacles(noSpec, nomSpec, prixBaseSpec) values (?, ?, ?);",
                    [self.selected_row[0].text()])
            except Exception as e:
                display.refreshLabel(self.ui.status,"Erreur de supression : "+repr(e))
                pass
            else:
                display.refreshLabel(self.ui.status,"Le spectacle {0} a été supprimé.".format(self.selected_row[0].text()))
                self.refreshResult()
                pass