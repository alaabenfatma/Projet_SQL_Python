import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from actions.action_add_rep import AppAddRep
from actions.action_modify_rep import AppModifRep
from actions.action_get_value import AppGetValue
# Classe permettant d'afficher la fonction à compléter 1
class AppEditRep(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/rep_edit.ui", self)
        self.data = data
        self.rep_ajout = None
        self.rep_modif = None
        self.rep_search = None
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT * FROM LesRepresentations;")
        except Exception as e:
            self.ui.table.setRowCount(0)
            display.refreshLabel(self.ui.status, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table, result)
    def open_search(self):
        if self.rep_search is not None:
                self.rep_search.close()
        self.rep_search = AppGetValue(self.data,self,"N° du spectacle associé avec: ")
        self.rep_search.show()
    def search(self,x):
        try:
            cursor = self.data.cursor()
            if(x!=""):
                result = cursor.execute("SELECT * FROM LesRepresentations where nospec LIKE ?;",[x])
            else:
                result = cursor.execute("SELECT * FROM LesRepresentations;")
        except Exception as e:
            self.ui.table.setRowCount(0)
            #display.refreshLabel(self.ui.label_fct_comp_1, "Impossible d'afficher les résultats : " + repr(e))
            print("Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table, result)
    def ajout(self):
            if self.rep_ajout is not None:
                self.rep_ajout.close()
            self.rep_ajout = AppAddRep(self.data,self)
            self.rep_ajout.show()
    def modify(self):
        #N'oubliez pas de selectionner une ligne avant de cliquer sur modifier.
            if self.rep_modif is not None:
                self.rep_modif.close()
            self.rep_modif = AppModifRep(self.data,self,self.ui.table.selectedItems()[0].text(),
                self.ui.table.selectedItems()[1].text(),self.ui.table.selectedItems()[2].text())
            self.rep_modif.show()

    def delete(self):
        #N'oubliez pas de selectionner une ligne avant de cliquer sur supprimer.
        try:
            self.selected_row = self.ui.table.selectedItems()
        except Exception as e:
            display.refreshLabel(self.ui.status,"Il faut selectionner une représentation.")
        else:
            msg =  QMessageBox()
            msg.setWindowTitle("Suppression")
            msg.setText("Voulez-vous vraiment supprimer ce spectacle?")
            msg.setStandardButtons(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            c =  self.data.cursor()
            req = "select count(*) from lestickets where nospec = ? and daterep=?"
            res = c.execute(req,[self.selected_row[0].text(),self.selected_row[1].text()])
            self.no_spec = int(self.selected_row[0].text())
            self.date_rep =self.selected_row[1].text()
            print(self.no_spec)
            self.num_of_tickets = list(res)[0][0]
            if(msg.exec() == QMessageBox.Yes):
                try:
                    result = c.execute("DELETE FROM LesRepresentations_base WHERE noSpec = ? and daterep =?",
                                    [self.no_spec, self.date_rep])
                    print(self.num_of_tickets)
                    if(self.num_of_tickets>0):
                        msg1 =  QMessageBox()
                        msg1.setWindowTitle("Suppression")
                        msg1.setText("Voulez-vous supprimer également les places associées a cette representation?")
                        msg1.setStandardButtons(QMessageBox.Yes)
                        msg1.addButton(QMessageBox.No)
                        msg1.setDefaultButton(QMessageBox.No)
                        if(msg1.exec() == QMessageBox.Yes):
                            try:
                                result = c.execute(
                                    "DELETE FROM Lestickets WHERE noSpec = ? and daterep=?",
                                    [self.no_spec, self.date_rep])
                            except Exception as e:
                                display.refreshLabel(self.ui.status,"Erreur de supression : "+repr(e))
                                print(repr(e))
                                pass
                            else:
                                display.refreshLabel(self.ui.status,"La representation associée au spectacle {0} a été supprimé.".format(self.no_spec))
                                pass
                except Exception as e:
                    display.refreshLabel(self.ui.status,"Erreur de supression : "+repr(e))
                    print(repr(e))
                    pass
                else:
                    display.refreshLabel(self.ui.status,"La representation  a été supprimé.")
                    self.refreshResult()
                    self.data.commit()
                    pass
        
        