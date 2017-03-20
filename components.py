# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:43:22 2017

@author: ACKWinDesk
"""
import tkinter as tk
import random

class TraitCard(object):
    """Frame containing trait card information"""
    # Use function and button
    # Includes use for food, use for trait, use for new species or upping pop, bs
    # configure command depending on phase or player action
    pass
    
class Foraging(TraitCard):
    pass

class LongNeck(TraitCard):
    pass

class Evolution(tk.Frame):    
    # Generate list of all cards in game
    all_cards = []
    all_cards.extend([Foraging() for i in range(20)])
    
    def __init__(self, num_players=3, master=None):
        tk.Frame.__init__(self, master)
        #self.title("Evolution")
        self.config(background='green')
        
        # Initialize game parameters
        
        # watering hole food
        self.food = 0

        # Deck of cards
        self.deck = Evolution.all_cards
        random.shuffle(self.deck)

        # Discard pile        
        self.discard = []
        
        # Set up information labels
        self.grid()
        #self.pack(fill='both',expand='true')
        self.food_label = tk.Label(self, text='Food on Watering Hole: ' +
                                              str(self.food))
        self.food_label.grid(row=0,column=0)                       
        #self.food_label.pack(side='left')  
        self.cards_left_label = tk.Label(self, text='Cards Left in Deck: ' + 
                                               str(len(self.deck)))
        self.cards_left_label.grid(row=0,column=1)
        #self.cards_left_label.pack(side='left')
                
        # Set up players
        self.num_players = num_players
        #self.players = [Player(self) for i in range(self.num_players)]
        self.players = [AI_Player(self) for i in range(self.num_players-1)]
        self.players.append(Human_Player(self))
#        for player in self.players:
#            player.grid()
        
        # make this random
        self.first_player = 0 % self.num_players  # current first player
        
        self.trait_limit = 3
        if self.num_players == 2: # special rules for 2 player
            self.trait_limit = 2
            # randomly remove 40 cars

    def plant_food(self):
        """Collect food cards"""
        pass
# Update First Player

        # Deal cards
        
        # populate food

class Hand(tk.Frame):
    """Frame containing players' hands. For humans, display frame"""
    # list of trait cards
    pass        

class Player(tk.Frame):
    """Defines base player. Mechanics of playing. Child classes define special
    humand and AI GUI elements"""
    def __init__(self, game):
        tk.Frame.__init__(self,game)
        # Ecosystem is a list of species
        self.master = game
        """Active Player Flag?"""
        self.num_species = 1
        self.num_cards = 0
        self.food_eaten = 0
        #self.label = tk.Label(self, text='Number of ')
        #self.label.grid(row=2,column=0)
        #self.label.grid()
        #self.grid(columnspan=1)
        self.grid(sticky='W')
        #self.pack(side='top')
        self.pop_label = tk.Label(self, text="Population: ")
        self.bs_label = tk.Label(self, text="Body Size: ")
        #self.pop_label.pack()
        #self.bs_label.pack()
        self.pop_label.grid(row=0,column=0, rowspan=2, columnspan=1, sticky='NW')
        self.bs_label.grid(row=1,column=0, rowspan=2, columnspan=1, sticky='NW')
        
        # Setup Ecosystem        
        self.ecosystem = [Species(self)]
        
        #Place species frames
        self.ecosystem[0].grid(row=0, column=1, sticky='E',rowspan=2)

        # Add "add species" buttons left and right        
        
        ## add label for population and bodysize for all species
        # Active player border highlight
        
    def modify_species(self, attribute, species_index):
        """attribute -> 'p' for population, 's' for body size
           species_index -> index of species in ecosystem"""
        try:
            if attribute == 'p':
                self.ecosystem[species_index].add_population()
            elif attribute == 's':
                self.ecosystem[species_index].add_body_size()
        except (BodySizeOverflowException, PopulationOverflowException):
            print("Cannot perform that action")
            
#    # Actions    
#    # Discard to add new species to ecosystem
#    def add_species_left(trait):
#        pass
#    def add_species_right(trait):
#        pass
#
#    # Add trait to species
#    def add_trait(trait, species_index):

    # Discard to improve existing species    
    
class Human_Player(Player):
    """Player with buttons to modify species and a hand showing"""
    def __init__(self, game):
        Player.__init__(self, game)
        self.config(background='yellow')
#        self.grid(columnspan=2)
#        # Display Ecosystem
#        self.update_ecosystem()
#        
#    def update_ecosystem(self):
#        self.eco_frames = []  # list the frames for each species
#
#        # delete old ecosystem?
#        i=0
#        for species in self.ecosystem:
#            species_frame = tk.Frame(self)
#            species_pop = tk.StringVar()
#            species_bs = tk.StringVar()
#            species_pop.set("Population: " + str(species.population))
#            species_bs.set("Body Size: " + str(species.body_size))
#            species_frame.grid(row=0,column=i)
#            species_frame.population_button = tk.Button(species_frame, 
#                                              textvariable=species_pop,
#                                              command=lambda i=i: self.modify_species('p',i))
#            species_frame.body_size_button = tk.Button(species_frame, 
#                                             textvariable=species_bs,
#                                             command=lambda i=i: self.modify_species('s',i))
#            species_frame.population_button.grid()                                               
#            species_frame.body_size_button.grid()
#            self.eco_frames.append(species_frame)
#            i+=1
    # Show hand

class AI_Player(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self.config(background='blue')
#        self.grid(columnspan=2)
#        self.eco_frames = []
#        # Display Ecosystem
#        i=0
#        for species in self.ecosystem:
#            species_frame = tk.Frame(self)
#            species_frame.grid(row=0,column=i)
#            species_frame.population_label = tk.Label(species_frame, 
#                                               text="Population: " + 
#                                               str(species.population))
#            species_frame.body_size_label = tk.Label(species_frame, 
#                                               text="Body Size: " + 
#                                               str(species.body_size))
#            species_frame.population_label.grid()                                               
#            species_frame.body_size_label.grid()
#            self.eco_frames.append(species_frame)
#            i+=1
#    def take_turn():
        pass
    def feed():
        pass
    
    # Show number of cards in hand
    
    
class Species(tk.Frame):
    def __init__(self, player):
        tk.Frame.__init__(self, player)
        self.master = player # which player owns this species
        self.human = False
        # check if player is human (because human species have active buttons)
        if isinstance(self.master, Human_Player): # better way to do this?
            self.human = True    
        self.carnivore = False    # carnivore flag
        self.population = 1
        self.body_size = 1
        
#        self.population = tk.IntVar()
#        self.population.set(1)
#        self.body_size = tk.IntVar()
#        self.body_size.set(1)
        self.traits = {}          # trait set

#        self.pack()
        self.population_button = tk.Button(self, text=self.population,
                                         command=self.command('p'))
        self.body_size_button = tk.Button(self, text=self.body_size,
                                         command=self.command('s'))                         
        self.population_button.grid()
        self.body_size_button.grid()
        #self.population_button.pack()
        #self.body_size_button.pack()

    def command(self, stat):
        """Button command for species depending on human player or not"""
        if self.human:
            if stat == 'p':
                return self.add_population
            elif stat == 's':
                return self.add_body_size
        else:
            return None
                
    def add_population(self):
        """Increase population by 1"""
        if self.population >= 6:
            raise PopulationOverflowException("Cannot add more than 6 population")
        else:
            self.population += 1
            self.population_button.config(text=self.population)

    def add_body_size(self):
        """Increase body size by 1"""
        if self.body_size >= 6:
            raise BodySizeOverflowException("Cannot add more than 6 body size")
        else:
            self.body_size += 1
            self.body_size_button.config(text=self.body_size)

    def feed(self):
        """Feed this species from either the watering hole or another species"""
        pass
    
    def starve(self):
        """Reduce population to fed level"""
        pass        
        
    def check_if_full(self):
        """Check if current food is less than population"""
        pass
    
#        self.grid()
#        self.population_label = tk.Label(self, text='0')
#        self.body_size_label = tk.Label(self, text='0')
#        self.population_label.pack(side="left")
#        self.body_size_label.pack()

        #self.label.grid(row=10,column=10)

#    # remove a trait    
#    def del_trait(trait):
#        
#    # add trait 
#    def add_trait(trait):
#        # check if traits would exceed trait limit    
#        if len(self.traits) == 3:
#            raise TraitOverflowException("You must first remove a trait before"
#                                         " adding a new one" )
#        # or if trait exists
#        elif trait in self.traits:
#            raise TraitRepeatException("You already have that trait on this "
#                                       "species")
#            
#    # check if full
#    # feed 

class BodySizeOverflowException(Exception):
    pass 

class PopulationOverflowException(Exception):
    pass 
   
class TraitOverflowException(Exception):
    pass

class TraitRepeatException(Exception):
    pass


game = Evolution()
game.mainloop()
#
#def main(): #run mainloop 
#    game = Evolution()
#    game.mainloop()
#
#if __name__ == '__main__':
#    main()