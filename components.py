# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:43:22 2017

@author: ACKWinDesk

Possible Issues:
    All widgets have parent instance as attribute
    
Future changes:
    Make things that can be pressed inactive
"""
import tkinter as tk
import random
from buttons import *


class Evolution(tk.Frame):    
    # Generate list of all cards in game
    all_cards = []
    all_cards.extend([Foraging() for i in range(20)])
    TRAIT_LIMIT = 3
    TRAIT_LIMIT_2p = 2
    BASE_CARD_DRAW = 3
    PHASE_NAMES = ["PLANT","EVOLVE","FEED"]
    
    def __init__(self, master=None, num_players=3, first_player=None):
        tk.Frame.__init__(self, master)
        #self.title("Evolution")
        self.config(background='green')
        
        # Initialize game parameters
        self.continue_game = True  # While true, game keeps going
        self.phase = tk.IntVar()   # current game phase?
        self.phase.set(-1)
        self.phase.trace('w', self.gui_phase_change)
        #self.food_on_hole = 0 # watering hole food
        self.food_on_hole = tk.IntVar() # watering hole food
        self.food_on_hole.set(0)

        # Deck of cards
        self.deck = Evolution.all_cards
        random.shuffle(self.deck)

        # Discard pile        
        self.discard = []
        
        ### BUILD GUI ####
        self.grid()
        # Set up information labels
        self.cards_left = tk.StringVar()
        self.era = tk.IntVar()
        self.phase_name = tk.StringVar()
        self.phase_name.set("GAME SETUP")
        
        self.cards_left_label = tk.Label(self, textvariable=self.cards_left)
        self.era_label1 = tk.Label(self, text="Era: ")
        self.era_label2 = tk.Label(self, textvariable=self.cards_left)
        self.phase_label1 = tk.Label(self, text="Phase: ")
        self.phase_label2 = tk.Label(self, textvariable=self.phase_name)
        self.food_label1 = tk.Label(self, text='Food on Watering Hole: ')
        self.food_label2 = tk.Label(self, textvariable=self.food_on_hole)
        
        self.cards_left_label.grid(row=0,column=0)
        self.era_label1.grid(row=0,column=1)
        self.era_label2.grid(row=0,column=2)
        self.phase_label1.grid(row=0,column=3)
        self.phase_label2.grid(row=0,column=4)
        self.food_label1.grid(row=0,column=5)
        self.food_label2.grid(row=0,column=6)
                
        # Set up players
        self.num_players = num_players
        #self.players = [Player(self) for i in range(self.num_players)]
        self.players = [AI_Player(self) for i in range(self.num_players-1)]
        self.players.append(Human_Player(self))
#        for player in self.players:
#            player.grid()

        # Set starting player        
        if first_player is None:
            first_player = random.randint(0, self.num_players-1)
        self.first_player = first_player  # current first player

        self.trait_limit = Evolution.TRAIT_LIMIT
        if self.num_players == 2: # special rules for 2 player
            self.trait_limit = Evolution.TRAIT_LIMIT_2p
            # randomly remove 40 cars

    def gui_phase_change(self):
        """Make certain widgets inactive during different game phases"""
        self.phase.get()
        self.phase_name.set(Evolution.PHASE_NAMES[self.phase.get()])
        pass 
    
    def play_game(self):
        """Loop phases until game over condition"""
        while(self.continue_game):
            self.deal_cards()
            self.plant_food()
            self.evolve()
            self.feed()
            # update current `first player
            self.first_player = self.index_wrap(1)
            self.era.set(self.era.get()+1)
            
    def index_wrap(self, k):
        """Compute player index wrapped"""
        return (self.first_player + k) % self.num_players  

    def check_for_empty_deck(self):
        """Check if deck is empty. 
        If it is, reshuffle discard and signal end of game"""
        if not self.deck:
            self.deck = self.discard
            random.shuffle(self.deck)
            self.discard = []
            self.continue_game = False
            
    def deal_cards(self):
        """Deal cards to each player. All cards required then to next player
        if that matters to you"""
        for i in range(0, self.num_players):
            # start at first player index
            player = self.players[self.index_wrap(i)]
            for c in range(Evolution.BASE_CARD_DRAW + player.num_species):
                self.check_for_empty_deck()
                # actually pops last element so pretend deck is flipped
                player.hand.add_card(self.deck.pop())
        if self.continue_game:
            self.cards_left.set('Cards Left in Deck: ' + len(self.deck))
        else:
            self.cards_left.set(0)

    def plant_food(self):
        """Collect food cards and add food to watering hole"""
        self.phase.set(0)
        pass
    
    def evolve(self):
        """Allow each player to evolve his ecosystem"""
        # Start with first player
        self.phase.set(1)

        #self.first_player
        
        # Autopass turn if no cards left for player
        
        
        pass
    
    def feed(self):
        """Allow players to eat food"""
        self.phase.set(2)
        # Start with first player
        #self.first_player
        pass
        

class TraitCard(tk.Frame, name="None", ability="None", food=0):
    """Frame containing trait card information"""
    # Need a database to load trait cards from

    def __init__(self, hand):
        tk.Frame.__init__(self, hand)
        self.master = hand
        self.name = name
        self.ability = ability
        self.food = food   # food that can be planted
        self.create_widgets()
        
    def create_widgets(self):
        """Create Trait Card GUI elements"""
        self.name_label = tk.Label(self, text=self.name)
        self.ability_label = tk.Label(self, text=self.ability)
        self.food_label = tk.Label(self, text="Food Eaten: ")
        self.use_button = TraitUseButton(self, text="USE", command=self.use)
        
        self.name_label.grid()  
        self.ability_label.grid()  
        self.food_label.grid()  
        self.use_button.grid()  
        
    def remove_from_hand(self):
        """Remove this frame from hand frame"""
        pass
                                         
    def use(self):
        """Signal to hand that this card was used"""
        master.use_trait_card(self)


class Hand(tk.Frame):
    """Frame containing players' hands. 
    For humans, display frame below player's species"""
    def __init__(self, player):
        tk.Frame.__init__(self, player)
        self.master = player
        self.empty = tk.BooleanVar()
        self.empty.set(True)
        self.empty.trace('w', self.toggle_empty_hand)
        self.num_cards = 0
        self.card_list = []

    def add_card(self, card):
        """Add card to hand"""
        self.card_list.append(card)
        if self.empty.get() is True:
            self.empty.set(False)    
            
    def activate_hand(self):
        pass

    def disable_hand(self):
        for widget in self.winfo_children():
            widget.config(state='disabled')
    
    def toggle_empty_hand(self):
        """Disable buttons if hand is empty"""
        # (depending on phase i.e. intelligence
        pass

    def use_trait_card(self, card):
        """Use trait card from hand for a variety of things"""
        # remove card from the list
        self.num_cards -= 1        
        temp = self.card_list.pop(self.card_list.index(card))
        if self.num_cards == 0:
           self.empty.set(True) 
        #check if hand is now empty
        return temp
        # Use function and button
        # Includes use for food, use for trait, use for new species or upping pop, bs
        # configure command depending on phase or player action 
        # use class variable?

    def update_hand(self):
        # update after dealt cards or when a card is used
        pass

class Player(tk.Frame):
    """Defines base player. Mechanics of playing. Child classes define special
    humand and AI GUI elements"""
    def __init__(self, game):
        tk.Frame.__init__(self,game)
        self.master = game
        self.active_player = tk.BooleanVar()
        self.active_player.set(False)
        self.active_player.trace('w', self.change_player_state)
        self.num_species = 1
        self.food_eaten = 0
        
        # need label for number of cards in hand
        
        # food stored
        # pass button
        
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
        
        # Setup Ecosystem (a list of species)
        self.ecosystem = [Species(self)]
        
        #Place species frames
        self.ecosystem[0].grid(row=0, column=1, sticky='E',rowspan=2)

        # Add "add species" buttons left and right        
        
        ## add label for population and bodysize for all species
        # Active player border highlight
        
        def update_species_frames(self):
            """Update species frames if some have gone extinct?"""
            pass
        
        def change_player_state(self):
            """Change player button states depending on if active player"""
            if self.active_player.get() is True:
                # Get game phase and unlock respective buttons?
                # or should game do that
                pass
            else:
                #shutdown buttons?
                pass
            
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
    # Show hand

class AI_Player(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self.config(background='blue')

    def take_turn():
        pass
    def feed():
        pass
    
    # Show number of cards in hand
    
    
class Species(tk.Frame):
    MAX_POP = 6    # max population
    MAX_SIZE = 6   # max body size
    def __init__(self, player):
        tk.Frame.__init__(self, player)
        self.master = player # which player owns this species
        self.human = False
        # check if player is human (because human species have active buttons)
        if isinstance(self.master, Human_Player): # better way to do this?
            self.human = True    
        self.carnivore = False    # carnivore flag

        self.hungry = True
        
        self.food = tk.IntVar()
        self.food.set(0)
        self.food.trace('w', self.set_food_dependent_flags)
        
        self.population = tk.IntVar()
        self.population.set(1)
        self.population.trace('w', self.set_population_dependent_flags)

        self.body_size = tk.IntVar()
        self.body_size.set(1)
        
        self.traits = {}          # trait set
        self.create_widgets()
        
    def create_widgets(self):
        """Create Species GUI elements"""
        self.feed_button = FeedButton(self, text="FEED")
        self.food_label1 = tk.Label(self, text="Food Eaten: ")
        self.food_label2 = tk.Label(self, textvariable=self.food)
        self.eat_button = EatButton(self, text="EAT ME")
        self.add_trait_buttons = []
        self.add_trait_labels = []
        for t in range(master.master.trait_limit):
            self.add_trait_buttons.append(AddTraitButton(self,text="Add Trait"))
            self.add_trait_labels.append(tk.Label(self, text="No Trait"))
        self.population_label1 = tk.Label(self, text="Population: ")
        self.population_label2 = tk.Label(self, textvariable=self.population)
        self.body_size1 = tk.Label(self, text="Body Size: ")
        self.body_size2 = tk.Label(self, textvariable=self.body_size)
        self.add_population_button = AddPopulationButton(self, text="+1 Population",
                                         command=self.add_population)
        self.add_body_size_button = AddBodySizeButton(self, text="+1 Body Size",
                                         command=self.add_body_size)  
                                         
        self.feed_button.grid(row=0,column=0)           
        self.food_label1.grid(row=0,column=1)   
        self.food_label2.grid(row=0,column=2)   
        self.eat_button.grid(row=0,column=3)         
        for t in range(master.master.trait_limit):            
            self.add_trait_buttons[t].grid(row=t+1,column=0)
            self.add_trait_labels[t].grid(row=t+1,column=1,columnspan=3)       
                                         
        self.population_label1.grid(row=5,column=0)
        self.population_label2.grid(row=5,column=1)
        self.body_size1.grid(row=5,column=2)
        self.body_size2.grid(row=5,column=3) 
        self.add_population_button.grid(row=6,column=0,columnspan=2)
        self.add_body_size_button.grid(row=6,column=2,columnspan=2)

    def set_food_dependent_flags(self):
        """Set flags depending on how much food is eaten"""
        # check if self.food <= self.population
        # change self.hungry
        pass
    
    def set_pop_dependent_flags(self):
        """Set flags depending on how much pop there is"""
        # check if self.food <= self.population
        # change self.hungry
        # change if population can be added (6)
        if self.population.get() == Species.MAX_POP:
            # turn off add population button
            pass
    
    def disable_all_buttons(self):
        """Disable all buttons in this species"""      
        for widget in self.winfo_children():
            widget.config(state='disabled')
        pass
                    
    def add_population(self):
        """Increase population by 1"""
        # First, check if less than max size
        if self.population.get() >= Species.MAX_POP:
            raise PopulationOverflowException("Cannot add more than 6 population")         
        self.population.set(self.population.get()+1)

    def add_body_size(self):
        """Increase body size by 1"""
        if self.body_size.get() >= Species.MAX_SIZE:
            raise BodySizeOverflowException("Cannot add more than 6 body size")
        self.body_size.set(self.body_size.get()+1)


    def feed(self):
        """Feed this species from either the watering hole or another species"""
        # or intelligence discard
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