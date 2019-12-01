
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from actions.action_res_ajout import AppResAjout
from actions.action_get_value import AppGetValue
# Classe permettant d'afficher la fonction à compléter 1
class AppResEdit(QDialog):

    res_ajout_dialog = None
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/res_edit.ui", self)
        self.data = data
        self.refreshResult()
        self.tick_search = None

    def open_res_ajout(self):
        if self.res_ajout_dialog is not None:
            self.res_ajout_dialog.close()
        self.res_ajout_dialog = AppResAjout(self.data,self)
        self.res_ajout_dialog.show()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        display.refreshLabel(self.ui.status, "")
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
    def open_search(self,parent):
        if self.tick_search is not None:
                self.tick_search.close()
        self.tick_search = AppGetValue(self.data,self,"Date d'emision du ticket : ")
        self.tick_search.show()
    def search(self,x):
        try:
            x= x+"%"
            cursor = self.data.cursor()
            if(x!=""):
                result = cursor.execute("SELECT noSpec, dateRep, noPlace, noRang, dateEmTick, libelleCat, noDos FROM LesTickets where dateEmTick LIKE ?",[x])
            else:
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
    def delete(self):
        display.refreshLabel(self.ui.status,"")
        self.selected_row = self.ui.table.selectedItems()
        msg =  QMessageBox()
        msg.setWindowTitle("Suppression")
        msg.setText("Voulez-vous vraiment supprimer ce ticket?")
        msg.setStandardButtons(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        self.no_spec = self.selected_row[0].text()
        self.date_rep = self.selected_row[1].text()
        self.noplace = self.selected_row[2].text()
        self.norang = self.selected_row[3].text()
        self.norang = self.selected_row[3].text()
        if(msg.exec() == QMessageBox.Yes):
            try:
                result = self.data.cursor().execute(
                    "DELETE FROM LesTickets WHERE noSpec = ? and dateRep = ? and noplace = ? and norang = ?",
                    [self.no_spec,self.date_rep,self.noplace,self.norang])
            except Exception as e:
                display.refreshLabel(self.ui.status,"Ereur : "+repr(e))
                pass
            else:
                display.refreshLabel(self.ui.status,"Le ticket a été supprimé.")
                self.refreshResult()
                self.data.commit()
                pass
