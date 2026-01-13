"""
RE1016 Assignment 2 by Yeo Shu Yi (REP).

PEP8 formatting standard used.
Comments ommitted wherever purpose is obvious.
Please refer to readme.md for setup and documentation.
"""


import pygame
from PIL import Image
import time
import pandas as pd


DATABASE_PATH = "./canteens.xlsx"


class CanteenQuery:
    """All query related functions defined within the class."""

    def __init__(self):
        """Initialise DB with extraction of keyword, price and location."""
        self.canteen_data = pd.read_excel(DATABASE_PATH)
        self.canteen_names = sorted(self.canteen_data['Canteen'].unique(), key=str.lower)
        self.canteen_stalls = sorted(self.canteen_data['Stall'].unique(), key=str.lower)

        if __debug__: print("Database Loaded.")

        # Keyword, price and location generation

        self.keywords = {}
        self.prices = {}
        for canteen in self.canteen_names:
            self.keywords[canteen] = {}
            self.prices[canteen] = {}
        
        copy_stall = self.canteen_data.copy()
        copy_stall.drop_duplicates(subset="Stall", inplace=True)
        stall_canteen_intermediate = copy_stall.set_index('Stall')['Canteen'].to_dict()
        stall_keywords_intermediate = copy_stall.set_index('Stall')['Keywords'].to_dict()
        stall_prices_intermediate = copy_stall.set_index('Stall')['Price'].to_dict()

        for stall in self.canteen_stalls:
            stall_canteen = stall_canteen_intermediate[stall]
            stall_keywords = stall_keywords_intermediate[stall]
            stall_price = stall_prices_intermediate[stall]
            self.keywords[stall_canteen][stall] = stall_keywords
            self.prices[stall_canteen][stall] = stall_price

        self.canteen_locations = {}
        for canteen in self.canteen_names:
            copy_canteen = self.canteen_data.copy()
            copy_canteen.drop_duplicates(subset="Canteen", inplace=True)
            canteen_locations_intermediate = copy_canteen.set_index('Canteen')['Location'].to_dict()
            self.canteen_locations[canteen] =  [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                                int(canteen_locations_intermediate[canteen].split(',')[1])]

        if __debug__: print("Keyword, Price and Location Generation Done.")
        


        
