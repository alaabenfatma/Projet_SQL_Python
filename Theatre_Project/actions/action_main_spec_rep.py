
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from actions.action_edit_spec import AppEditSpec
from actions.action_edit_rep import AppEditRep

# Classe permettant d'afficher la fonction à compléter 1
class AppMainSpecRep(QDialog):
    
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/main_spec_rep.ui", self)
        self.data = data
        self.spec_dialog = None
        self.rep_dialog = None

    def open_spec(self):
        if self.spec_dialog is not None:
            self.spec_dialog.close()
        self.spec_dialog = AppEditSpec(self.data)
        self.spec_dialog.show()
    def open_rep(self):
        if self.rep_dialog is not None:
            self.rep_dialog.close()
        self.rep_dialog = AppEditRep(self.data)
        self.rep_dialog.show()
    