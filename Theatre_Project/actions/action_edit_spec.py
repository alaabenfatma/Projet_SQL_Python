import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from actions.action_add_spec import AppAddSpec
from actions.action_modify_spec import AppModifSpec
# Classe permettant d'afficher la fonction à compléter 1
class AppEditSpec(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/spec_edit.ui", self)
        self.data = data
        self.spec_ajout = None
        self.spec_modif = None
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
    def modify(self):
            if self.spec_modif is not None:
                self.spec_modif.close()
            self.spec_modif = AppModifSpec(self.data,self,self.ui.table.selectedItems()[0].text())
            self.spec_modif.show()

    def delete(self):
        self.selected_row = self.ui.table.selectedItems()
        msg =  QMessageBox()
        msg.setWindowTitle("Suppression")
        msg.setText("Voulez-vous vraiment supprimer ce spectacle?")
        msg.setStandardButtons(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        c =  self.data.cursor()
        req = "select count(*) from lestickets where nospec = ?"
        res = c.execute(req,[self.selected_row[0].text()])
        self.no_spec = self.selected_row[0].text()
        self.no_spec = int(self.no_spec)
        print(self.no_spec)
        if(msg.exec() == QMessageBox.Yes):
            try:
                result = c.execute(
                    "DELETE FROM LesSpectacles WHERE noSpec = ?",
                    [self.no_spec])
                if(int(list(res)[0][0])>0):
                    msg1 =  QMessageBox()
                    msg1.setWindowTitle("Suppression")
                    msg1.setText("Voulez-vous supprimer également les representations et les places associées a ce spectacle?")
                    msg1.setStandardButtons(QMessageBox.Yes)
                    msg1.addButton(QMessageBox.No)
                    msg1.setDefaultButton(QMessageBox.No)
                    if(msg1.exec() == QMessageBox.Yes):
                        try:
                            result = c.execute(
                                "DELETE FROM LesRepresentations_base WHERE noSpec = ?",
                                [self.no_spec])
                            result = c.execute(
                                "DELETE FROM Lestickets WHERE noSpec = ?",
                                [self.no_spec])
                        except Exception as e:
                            display.refreshLabel(self.ui.status,"Erreur de supression : "+repr(e))
                            print(repr(e))
                            pass
                        else:
                            display.refreshLabel(self.ui.status,"Le spectacle {0} a été supprimé.".format(self.no_spec))
                            self.refreshResult()
                            self.data.commit()
                            pass
            except Exception as e:
                display.refreshLabel(self.ui.status,"Erreur de supression : "+repr(e))
                print(repr(e))
                pass
            else:
                display.refreshLabel(self.ui.status,"Le spectacle {0} a été supprimé.".format(self.no_spec))
                self.refreshResult()
                self.data.commit()
                pass
        
        