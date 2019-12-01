import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDateTime
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppModifRep(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection,parent,nospec,old_date,promo):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/rep_modify.ui", self,)
        self.data = data
        self.parent = parent
        self.nospec=nospec
        self.ui.num.setValue(int(nospec))
        self.ui.date.setDateTime(QDateTime.fromString(old_date,"dd/MM/yyyy hh:mm"))
        self.ui.promo.setValue(float(promo))
        self.old_date = old_date
        
    def update(self):
        display.refreshLabel(self.ui.status, "")
        nospec = self.ui.num.text().strip()
        d = self.ui.date.dateTime().toString("dd/MM/yyyy hh:mm")
        promo = self.ui.promo.text().strip()
        cursor = self.data.cursor()
        res = self.data.cursor().execute(
                    "select count(nospec) from LesSpectacles where nospec = ?",[nospec])
        if(int(list(res)[0][0])==0):
             display.refreshLabel(self.ui.status, "Il y a pas un spectale avec le nospec {0}".format(nospec))
        else:
            try:
                result = cursor.execute(
                    "UPDATE LesRepresentations_base SET nospec = ?, daterep= ?, promorep = ? WHERE nospec = ? AND daterep = ?;",
                    [nospec,d,promo,self.nospec,self.old_date])
                self.old_date = d
                self.nospec = nospec
            except Exception as e:
                print( "Impossible d'afficher les résultats : " + repr(e))
                display.refreshLabel(self.ui.status, "Impossible d'afficher les résultats : " + repr(e))
            else:
                display.refreshLabel(self.ui.status, "Representation modifiée avec succés")
                self.data.commit()
                self.parent.refreshResult()
                