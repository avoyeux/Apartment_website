"""
To save who owes what in a csv file.
"""

# Imports
import os
import glob

import pandas as pd




class STATS:


    def __init__(self):
        """
        The expenses.
        """

        # Monthly expenses
        self.loyer_mensuel_charges_comprises = 1222
        self.internet = None
        self.electricite = None
        self.assurance = None

        # One time expenses
        self.depot_de_garantie = 2144
        self.virement_pr_honoraires_agence = 845
        self.virement_prorata_mars = 946.06

    def Main(self):
        """
        Outputs who owes what.
        """

        payments = {'Alfred': 0, 'Farid': 0, 'Guarantor Alfred': 0, 'Guarantor Farid': 0}

        # Before the contract signing
        total = self.First_payement()
        payments['Alfred'] += total * 1
        payments['Farid'] += total * 0 # Alfred paid for everything this time 


        

    def First_payement(self):
        """
        First payment made (i.e. before even signing the contract).
        """

        Total = self.depot_de_garantie + self.virement_pr_honoraires_agence + self.virement_prorata_mars

