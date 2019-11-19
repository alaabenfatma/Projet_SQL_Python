
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesData(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/tablesData.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTables()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)


    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAllTables(self):

        self.refreshTable(self.ui.label_spectacles, self.ui.tableSpectacles, "SELECT noSpec, nomSpec, prixBaseSpec FROM LesSpectacles")
        self.refreshTable(self.ui.label_zones, self.ui.tableZones, "SELECT noZone, catZone, tauxZone  FROM LesZones")
        # TODO 1.2 : modifier pour afficher les éléments de la vue LesRepresentations
        self.refreshTable(self.ui.label_representations, self.ui.tableRepresentations, "SELECT noSpec, dateRep, promoRep FROM LesRepresentations_base")
        self.refreshTable(self.ui.label_places, self.ui.tablePlaces, "SELECT noPlace, noRang, noZone FROM LesPlaces")
        # TODO 1.4 : modifier pour afficher les éléments de la vue LesDossiers
        self.refreshTable(self.ui.label_dossiers, self.ui.tableDossiers, "SELECT noDos FROM LesDossiers_base")
        self.refreshTable(self.ui.label_tickets, self.ui.tableTickets, "SELECT noSpec, dateRep, noPlace, noRang, dateEmTick, noDos FROM LesTickets")
        # TODO 1.3 : vérifier le bon fonctionnement de la requête pour afficher le contenu de la table LesCategoriesTickets
        self.refreshTable(self.ui.label_categories, self.ui.tableCategories, "SELECT libelleCat, tauxReductionCat FROM LesCategoriesTickets")