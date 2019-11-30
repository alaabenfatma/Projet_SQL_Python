import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppAddRep(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection,parent):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/rep_ajout.ui", self)
        self.data = data
        self.rep_ajout = None
        self.parent = parent
    
    def ajout(self):
        num = self.ui.num.text().strip()
        date = self.ui.date.text()
        promo = self.ui.promo.text().strip()
        cursor = self.data.cursor()
        display.refreshLabel(self.ui.status, "")
        res = cursor.execute(
                    "select count(nospec) from LesSpectacles where nospec = ?",[num])
        if(int(list(res)[0][0])==0):
             display.refreshLabel(self.ui.status, "Il y a pas un spectale avec le nospec {0}".format(num))
        else:
            try:
                self.price = float(self.ui.promo.text().strip().replace(',','.'))
            except Exception as e:
                self.price = float(self.ui.promo.text().strip())
            else:
                try:
                    
                    result = cursor.execute(
                        "insert into LesRepresentations_base(noSpec, dateRep, promoRep) values (?, ?, ?);",
                        [num,date,promo])
                
                except Exception as e:
                    print( "Impossible d'afficher les résultats : " + repr(e))
                    display.refreshLabel(self.ui.status, "Impossible d'afficher les résultats : " + repr(e))
                else:
                    display.refreshLabel(self.ui.status, "Spectacle ajouté avec succés")
                    self.data.commit()
                    self.parent.refreshResult()
            