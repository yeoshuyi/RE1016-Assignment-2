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
IMAGE_PATH = "./NTUcampus.jpg"
PIN_PATH = "./pin.png"


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
        
    def get_user_location_interface(self):
        """Get user's location with PyGame"""

        SCREEN_TITLE = "NTU Map"

        image = Image.open(IMAGE_PATH)
        image_width_original, image_height_original = image.size
        scaled_width = int(image_width_original * 0.9)
        scaled_height = int(image_height_original * 0.9)
        
        pin_image = pygame.image.load(PIN_PATH)
        pin_image_scaled = pygame.transform.scale(pin_image, (60, 60))
        screen_image = pygame.image.load(IMAGE_PATH)
        screen_image_scaled = pygame.transform.scale(scaled_width, scaled_height)

        pygame.init()
        screen = pygame.display.set_mode([scaled_width, scaled_height])
        pygame.display.set_caption(SCREEN_TITLE)
        screen.blit(screen_image_scaled, (0,0))
        pygame.display.flip()

        while True:
            pygame.event.pump()
            event = pygame.event.wait()

            match event.type:
                case pygame.QUIT:
                    pygame.display.quit()
                    self.mouseX_scaled = None
                    self.mouseY_scaled = None
                    break

                case pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode(
                    event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                    screen.blit(pygame.transform.scale(screen_image_scaled, event.dict['size']), (0, 0))
                    scaled_height = event.dict['h']
                    scaled_width = event.dict['w']
                    pygame.display.flip()
                
                case pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    screen.blit(pin_image_scaled, (mouseX - 25, mouseY - 45))
                    pygame.display.flip()
                    self.mouseX_scaled = int(mouseX * 1281 / scaled_width)
                    self.mouseY_scaled = int(mouseY * 1550 / scaled_height)
                    time.sleep(0.2)
                    break
        
        pygame.quit()
        pygame.init()
        
        return 0
