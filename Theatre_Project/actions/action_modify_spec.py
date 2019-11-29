import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppModifSpec(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection,parent,nospec):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/spec_modify.ui", self)
        self.data = data
        self.parent = parent
        self.nospec = nospec
        result = data.cursor().execute(
                    "select * from lesspectacles where nospec = ?",
                    [self.nospec])
        res = list(result)
        self.name = ((res)[0][1])
        self.price = ((res)[0][2])
        self.ui.num.setValue(int(nospec))
        self.ui.nom.setText(str(self.name))
        self.ui.prix.setValue(float(self.price.replace(',','.')))

    def update(self):
        display.refreshLabel(self.ui.status, "")
        if((self.ui.nom.text=="") or( float(self.ui.prix.text().strip().replace(',','.')) == 0)):
            display.refreshLabel(self.ui.status, "Veuillez vérifier le nom du spectacle & le prix")
        else:
            try:
                num = self.ui.num.text().strip()
                nom = self.ui.nom.text()
                prix = self.ui.prix.text().strip()
                cursor = self.data.cursor()
                result = cursor.execute(
                    "insert into LesSpectacles(noSpec, nomSpec, prixBaseSpec) values (?, ?, ?);",
                    [num,nom,prix])
            
            except Exception as e:
                print( "Impossible d'afficher les résultats : " + repr(e))
                display.refreshLabel(self.ui.status, "Impossible d'afficher les résultats : " + repr(e))
            else:
                display.refreshLabel(self.ui.status, "Spectacle ajouté avec succés")
                self.data.commit()
                self.parent.refreshResult()
                