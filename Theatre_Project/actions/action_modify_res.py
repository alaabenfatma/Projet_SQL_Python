import sqlite3
import datetime
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppResModif(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection,parent,old_data):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/res_modif.ui", self)
        self.data = data
        self.cursor = self.data.cursor()
        self.refreshResult()
        #Mise a jour du formulaire
        for row in self.cursor.execute("SELECT max(nodos) FROM LesDossiers"):
            self.ui.spinBox.setMaximum(row[0])
        for row in self.cursor.execute('SELECT nomSpec FROM LesSpectacles'):
            self.ui.combo_sql_spec.addItem(row[0])
        index = self.ui.combo_sql_spec.currentIndex()
        for row in self.cursor.execute('SELECT dateRep FROM LesRepresentations NATURAL JOIN LesSpectacles WHERE nomSpec LIKE ?',[self.ui.combo_sql_spec.itemText(index)]):
            self.ui.combo_sql_rep.addItem(row[0])
        index2 = self.ui.combo_sql_rep.currentIndex()
        for row in self.cursor.execute('SELECT libelleCat FROM LesCategoriesTickets'):
            self.ui.comboBox_2.addItem(row[0])
        for row in self.cursor.execute('SELECT DISTINCT noPlace FROM LesPlaces'):
            self.ui.comboBox_3.addItem(str(row[0]))
        index3 = self.ui.comboBox_3.currentIndex()
        for row in self.cursor.execute('SELECT noRang FROM LesPlaces EXCEPT SELECT noRang FROM LesTickets NATURAL JOIN LesSpectacles WHERE nomSpec LIKE ? AND noPlace = ? AND dateRep LIKE ? ', [self.ui.combo_sql_spec.itemText(index), self.ui.comboBox_3.itemText(index3), self.ui.combo_sql_rep.itemText(index2)]):
            self.ui.comboBox_4.addItem(str(row[0]))
        self.parent = parent
        self.old_nodos = old_data[6].text()
        print(self.old_nodos)
        self.old_nospec = old_data[0].text()
        self.old_daterep = old_data[1].text()
        self.old_noplace = old_data[2].text()
        self.old_norang = old_data[3].text()
        self.old_dateem = old_data[4].text()
        self.old_lib = old_data[5].text()
        self.ui.spinBox.setValue(int(self.old_nodos))
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
    
    @pyqtSlot()
    def refreshResult2(self):
        self.ui.comboBox_4.clear()
        index = self.ui.combo_sql_spec.currentIndex()
        index2 = self.ui.combo_sql_rep.currentIndex()
        index3 = self.ui.comboBox_3.currentIndex()
        for row in self.cursor.execute('SELECT noRang FROM LesPlaces EXCEPT SELECT noRang FROM LesTickets NATURAL JOIN LesSpectacles WHERE nomSpec LIKE ? AND noPlace = ? AND dateRep = ? ', [self.ui.combo_sql_spec.itemText(index), self.ui.comboBox_3.itemText(index3), self.ui.combo_sql_rep.itemText(index2)]):
            self.ui.comboBox_4.addItem(str(row[0]))
    
    @pyqtSlot()
    def createTicket(self):
        display.refreshLabel(self.ui.status, "")
        now = datetime.datetime.now()
        noDos = self.ui.spinBox.text().strip()
        noSpec = self.ui.combo_sql_spec.currentText()
        dateRep = self.ui.combo_sql_rep.currentText()
        catPers = self.ui.comboBox_2.currentText()
        noPlace = self.ui.comboBox_3.currentText()
        noRang = self.ui.comboBox_4.currentText()
        try:
          
            
            if(noRang != ""):
                for row in self.cursor.execute("SELECT count(*) FROM LesTickets WHERE noDos = ?", [noDos]):
                    exists = row[0]
                if(exists == 0):
                    res = self.data.cursor().execute("SELECT max(nodos) FROM LesDossiers")
                    max_dos = list(res)[0][0] + 1
                    insert_max_dos = self.data.cursor().execute("insert into LesDossiers_base(noDos) values (?)",[max_dos])
                    result = self.cursor.execute(
                                "update LesTickets set nospec= (SELECT noSpec FROM LesSpectacles WHERE nomSpec LIKE ?), daterep= ?, noplace= ?,norang= ?,libelleCat= ?,nodos= ? where nospec = ?,noplace=?, norang=?",
                                [noSpec,dateRep,noPlace,noRang,catPers, max_dos,noSpec,noPlace,noRang])
                    noDos = max_dos
                else:
                    result = self.cursor.execute(
                                "update LesTickets set nospec= (SELECT noSpec FROM LesSpectacles WHERE nomSpec LIKE ?), daterep= ?, noplace= ?,norang= ?,libelleCat= ?,nodos= ? where nospec = ? and noplace=? and norang=?;",
                                [noSpec,dateRep,noPlace,noRang,catPers, noDos,self.old_nospec,self.old_noplace,self.old_norang])
            else:
                display.refreshLabel(self.ui.status,"Erreur : Le numero de rang est vide")
                return
        except Exception as e:
            display.refreshLabel(self.ui.status,"Erreur : "+ repr(e))
        else:
            display.refreshLabel(self.ui.status,"La reservation a été modifiée avec succès.")
            self.data.commit()
            self.parent.refreshResult()
            self.old_daterep =  dateRep
            self.old_lib = catPers
            self.old_nodos = noDos
            self.old_noplace = noPlace
            self.old_norang = noRang