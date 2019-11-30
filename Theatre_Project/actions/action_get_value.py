
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fonction à compléter 1
class AppGetValue(QDialog):
    
    # Constructeur
    def __init__(self, data:sqlite3.Connection,parent,field_name):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/get_value.ui", self)
        self.data = data
        self.parent = parent
        display.refreshLabel(self.ui.field,field_name)
    def returnVal(self):
        self.parent.search(self.ui.val.text())
    
    