import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppResAjout(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/res_ajout.ui", self)
        self.data = data
        self.cursor = self.data.cursor()
        self.refreshResult()
        for row in self.cursor.execute("SELECT count(*) FROM LesDossiers"):
            self.ui.spinBox.setMaximum(row[0])
        for row in self.cursor.execute('SELECT nomSpec FROM LesSpectacles'):
            self.ui.combo_sql_spec.addItem(row[0])
        index = self.ui.combo_sql_spec.currentIndex()
        for row in self.cursor.execute('SELECT dateRep FROM LesRepresentations NATURAL JOIN LesSpectacles WHERE nomSpec LIKE ?',[self.ui.combo_sql_spec.itemText(index)]):
            self.ui.combo_sql_rep.addItem(row[0])
        index2 = self.ui.combo_sql_rep.currentIndex()
        for row in self.cursor.execute('SELECT catZone FROM LesZones'):
            self.ui.comboBox.addItem(row[0])
        for row in self.cursor.execute('SELECT libelleCat FROM LesCategoriesTickets'):
            self.ui.comboBox_2.addItem(row[0])
        for row in self.cursor.execute('SELECT DISTINCT noPlace FROM LesPlaces'):
            self.ui.comboBox_3.addItem(str(row[0]))
        index3 = self.ui.combo_sql_rep.currentIndex()
        for row in self.cursor.execute('SELECT noRang FROM LesPlaces EXCEPT SELECT noRang FROM LesTickets NATURAL JOIN LesSpectacles WHERE nomSpec LIKE ? AND noPlace = ? AND dateRep = ? ', [self.ui.combo_sql_spec.itemText(index), self.ui.comboBox_3.itemText(index3), self.ui.combo_sql_rep.itemText(index)]):
            self.ui.comboBox_4.addItem(str(row[0]))
    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        self.ui.combo_sql_rep.clear()
        index = self.ui.combo_sql_spec.currentIndex()
        for row in self.cursor.execute('SELECT dateRep FROM LesRepresentations NATURAL JOIN LesSpectacles WHERE nomSpec LIKE ?',[self.ui.combo_sql_spec.itemText(index)]):
            self.ui.combo_sql_rep.addItem(row[0])
        try:
            cursor = self.data.cursor()
            # TODO 1.1 : mettre à jour la requête et changer aussi le fichier ui correspondant
            result = cursor.execute("SELECT * FROM LesTickets;")
        except Exception as e:
            #self.ui.table.setRowCount(0)
            #display.refreshLabel(self.ui.label_fct_comp_1, "Impossible d'afficher les résultats : " + repr(e))
            print("Impossible d'afficher les résultats : " + repr(e))