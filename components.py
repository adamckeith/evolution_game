# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:43:22 2017

@author: ACKWinDesk

Design:
    Only one human player or less currently intended
    If a button can be pressed, it is a logical move and does not have error
        checking. All possible moves are made available. 

Possible Issues:
    Do I really need setup_phase?
    
    
Future changes:
    Make things that can be shouldn't pressed inactive
    Make species gui a little more compact
    Nonzero cards in other players signals that they have yet to evolve 
        (how to weigh that?)
"""
import tkinter as tk
import random
from buttons import *
import time

class TraitCard(tk.Frame):
    """Frame containing trait card information"""
    # Need a database to load trait cards from
    def __init__(self, hand=None, name="None", ability="None", food=10):
        self.hand = hand
        self.name = name
        self.ability = ability
        self.food = food   # food that can be planted
        
    def create_widgets(self):
        """Create Trait Card GUI elements"""
        # only ever shown card in player's hand, so create widgets when dealt
        self.name_label = tk.Label(self, text=self.name)
        self.ability_label = tk.Label(self, text=self.ability)
        self.food_label = tk.Label(self, text="Food: " + str(self.food))
        self.use_button = TraitUseButton(self, text="USE", command=self.use)
        
    def pack_widgets(self):
        self.name_label.pack()  
        self.ability_label.pack()  
        self.food_label.pack()  
        self.use_button.pack()
        
    def dealt(self, new_hand=None):
        """Change master frame of this card"""
        # be careful because old_hand is still the master frame
        # but new_hand is the logical owner
        tk.Frame.__init__(self, new_hand)
        self.change_hands(new_hand)  
        self.create_widgets()
        self.pack_widgets()
  
    def change_hands(self, new_hand=None):
        """Change master frame of this card"""
        self.hand = new_hand
    
    def disable_use(self):
        """Disable use button"""
        self.use_button.config(state="disabled")
        
    def enable_use(self):
        """Enable use button"""
        self.use_button.config(state="normal")
        
    def remove_from_hand(self):
        """Remove this frame from hand frame"""
        pass
        
    def use(self):
        """Signal to hand that this card was used"""
        self.hand.use_trait_card(self)

class Evolution(tk.Frame):    
    # Generate list of all cards in game
    all_cards = []
    all_cards.extend([TraitCard() for i in range(20)]) 
    #more_cards = []
    #more_cards.extend([TraitCard() for i in range(10)]) 
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
        self.food_deck = []    # temporary place to store cards to plant food


        # Deck of cards
        self.deck = Evolution.all_cards
        for card in self.deck:
            card.change_hands(self)
        random.shuffle(self.deck)

        # Discard pile        
        self.discard = []
        
        # Set starting player        
        self.num_players = num_players
        if first_player is None:
            first_player = random.randint(0, self.num_players-1)
        self.first_player = first_player  # current first player

        self.trait_limit = Evolution.TRAIT_LIMIT
        if self.num_players == 2: # special rules for 2 player
            self.trait_limit = Evolution.TRAIT_LIMIT_2p
            # randomly remove 40 cars        
            
        self.cards_left = tk.IntVar()
        self.cards_left.set(len(self.deck))
        self.era = tk.IntVar()
        self.era.set(0)
        self.phase_name = tk.StringVar()
        self.phase_name.set("GAME SETUP")
        self.create_widgets()
        self.pack_widgets()
        
        # Set up players' frames
        #self.players = [Player(self) for i in range(self.num_players)]
        self.players = [AI_Player(self,i) for i in range(self.num_players-1)]
        ### ASSUMES ONLY ONE HUMAN PLAYER ####
        self.players.append(Human_Player(self,self.num_players-1))
        for player in self.players:
            player.pack(fill='both',expand=True,anchor="nw")
        #self.update()
        #self.after(5000,self.play_game())

    def create_widgets(self):
        ### BUILD GUI ####
        # Set up information labels
        self.game_information_frame = tk.Frame(self)
        gi = self.game_information_frame
        gi.pack(fill="x",expand=False,anchor="nw")
        self.cards_left_label1 = tk.Label(gi, text="Cards Left in Deck:", 
                                          fg='white', bg='black')
        self.cards_left_label2 = tk.Label(gi, textvariable=self.cards_left,
                                          fg='white', bg='black')
        self.era_label1 = tk.Label(gi, text="|Era:", fg='white', bg='black')
        self.era_label2 = tk.Label(gi, textvariable=self.era, 
                                   fg='white', bg='black')
        self.phase_label1 = tk.Label(gi, text="|Phase:",
                                     fg='white', bg='black')
        self.phase_label2 = tk.Label(gi, textvariable=self.phase_name,
                                     fg='white', bg='black')
        self.food_label1 = tk.Label(gi, text="|Food on Watering Hole:",
                                    fg='white', bg='black')
        self.food_label2 = tk.Label(gi, textvariable=self.food_on_hole,
                                    fg='white', bg='black')
                                    
    def pack_widgets(self):
        self.cards_left_label1.pack(side="left",fill='x',expand=True,anchor="nw")
        self.cards_left_label2.pack(side="left",fill='x',expand=True,anchor="nw")
        self.era_label1.pack(side="left",fill='x',expand=True,anchor="nw")
        self.era_label2.pack(side="left",fill='x',expand=True,anchor="nw")
        self.phase_label1.pack(side="left",fill='x',expand=True,anchor="nw")
        self.phase_label2.pack(side="left",fill='x',expand=True,anchor="nw")
        self.food_label1.pack(side="left",fill='x',expand=True,anchor="nw")
        self.food_label2.pack(side="left",fill='x',expand=True,anchor="nw")

    def gui_phase_change(self, *args):
        """Make certain widgets inactive during different game phases"""
        self.phase_name.set(Evolution.PHASE_NAMES[self.phase.get()])
        pass 
    
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
        # Don't actually set cards left until all cards have been handed out
        if self.continue_game:
            self.cards_left.set(len(self.deck))
        else:
            self.cards_left.set(0)

    def play_game(self):
        """Loop phases until game over condition"""
            # need everyone to pass to move to next phase?
        self.deal_cards()
        self.plant_food()
#        while(self.continue_game):
#            # need everyone to pass to move to next phase?
#            self.deal_cards()
#            self.plant_food()
#            self.evolve()
#            self.feed()
#            # update current `first player
#            self.first_player = self.index_wrap(1)
#            self.era.set(self.era.get()+1)
        

    def next_phase(self):
        self.phase.set((self.phase.get()+1) % len(Evolution.PHASE_NAMES))

    def pass_control_next(self, player=None):
        # depending on phase, pass control to the game
        # for example, once we get back to first player on plant phase, plant
        # the food
        if player is None:
            player=self.first_player
            
        if self.phase.get() == 0:
            if self.index_wrap(self.players.index(player)+1) == self.first_player:
                total = sum([f.food for f in self.food_deck])
                self.food_on_hole.set(self.food_on_hole.get()+total)
                self.discard.extend(self.food_deck)
                self.food_deck = []
                # pass control to next phase
            else:
                self.players[self.index_wrap(self.players.index(player)+1)].take_turn()
        
        # later phases, all players have no possible moves

    def broadcast_phase_change(self):
        """Setup new phase for all players"""
        # probably should make this a callback on players when self.phase is set
        for player in self.players:
            player.setup_phase()
            
    def plant_food(self):
        """Collect food cards and add food to watering hole"""
        self.phase.set(0)
        #self.broadcast_phase()
        self.players[self.first_player].take_turn()
    
            
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
        

class Hand(tk.Frame):
    """Frame containing players' hands. 
    For humans, display frame below player's species"""
    def __init__(self, player):
        tk.Frame.__init__(self, player)
        self.player = player
        self.empty = tk.BooleanVar()
        self.empty.set(True)
        self.num_cards = tk.IntVar()
        self.num_cards.set(0)
        self.card_list = []
        
    def add_card(self, card):
        """Add card to hand"""
        self.unpack_cards()
        card.dealt(self)
        self.card_list.append(card)
        self.num_cards.set(self.num_cards.get()+1)
        # pretty inefficient to unpack and pack on every card addition...
        self.pack_cards()  
        if self.empty.get() is True:
            self.empty.set(False)
            self.toggle_empty_hand()
            
    def pack_cards(self):
        """Pack card frames"""
        for card in self.card_list:
            card.pack(side="left")
        
    def unpack_cards(self):
        """Unpack card frames"""
        for card in self.card_list:
            card.pack_forget()

    def disable(self):
        for card in self.card_list:
            card.disable_use()
            
    def enable(self):
        for card in self.card_list:
            card.enable_use()
            
    def toggle_empty_hand(self):
        """Disable buttons if hand is empty"""
        # well if hand is empty, unpack it from player
        if self.empty.get() is True:
            self.pack_forget()
        else:
            self.player.pack_hand()  # bring it back
        # (depending on phase i.e. intelligence
        
    def use_trait_card(self, card):
        """Use trait card from hand for a variety of things"""
        # remove card from the list
        self.num_cards.set(self.num_cards.get()-1)
        self.card_list.remove(card)
        #temp = self.card_list.pop(self.card_list.index(card))
        #check if hand is now empty
        if self.num_cards.get() == 0:
           self.empty.set(True)
           self.toggle_empty_hand()
        card.pack_forget()           
        card.change_hands()  # forget that you belonged to this hand!
        self.player.make_payment(card)


class Player(tk.Frame):
    """Defines base player. Mechanics of playing. Child classes define special
    humand and AI GUI elements"""
    def change_player_state(self):
        """Change player button states depending on if active player"""
        if self.active_player.get() is True:
            # Get game phase and unlock respective buttons?
            # or should game do that
            pass
        else:
            pass
            #self.disable_all_buttons()
        
    def __init__(self, game, player_index):
        tk.Frame.__init__(self,game)
        self.game = game
        self.game.phase.trace('w', self.setup_phase)
        self.player_index = player_index
        self.active_player = tk.BooleanVar()
        self.active_player.set(False)
        self.active_player.trace('w', self.change_player_state)
        self.num_species = 1
        self.food_eaten = tk.IntVar()        
        self.food_eaten.set(0)
        self.payment_type = None  # string if player use, integer as an index
                                  # to species to give to
        self.ecosystem = []

        # This block order is very important to make the gui pack correctly        
        self.create_widgets()
        self.pack_player_info_frame()
        # instead of calling add species (because it requests payment)
        self.ecosystem.append(Species(self)) 
        self.pack_hand()
        self.pack_ecosystem()
        
        # Active player border highlight?
        
    def create_widgets(self):        
        self.hand = Hand(self)        
        self.player_info_frame = tk.Frame(self)
        pif = self.player_info_frame
        self.cards_in_hand_label1 = tk.Label(pif, text="Number of Cards: ")
        self.cards_in_hand_label2 = tk.Label(pif, textvariable=self.hand.num_cards)
        self.food_label1 = tk.Label(pif, text="Food in Bag:")
        self.food_label2 = tk.Label(pif, textvariable=self.food_eaten)
        self.pass_button = PassButton(pif,text="PASS", command=self.pass_player)

        self.add_species_left_button = AddSpeciesLeftButton(
                self, text="Add Species Left", 
                command=lambda:self.add_species('L'))
        self.add_species_right_button = AddSpeciesRightButton(
                self, text="Add Species Right", 
                command=lambda:self.add_species('R'))
                
    def pack_player_info_frame(self):
        """Pack Player information bar"""
        self.player_info_frame.pack(fill='x',expand=False,anchor="ne")
        self.cards_in_hand_label1.pack(side='left',fill='x',expand=True,anchor="nw")
        self.cards_in_hand_label2.pack(side='left',fill='x',expand=True,anchor="nw")
        self.food_label1.pack(side='left',fill='x',expand=True,anchor="nw")
        self.food_label2.pack(side='left',fill='x',expand=True,anchor="nw")
        self.pass_button.pack(side='left',fill='x',expand=True,anchor="nw")
    
    def pack_hand(self):
        """Pack hand"""
        self.hand.pack(side="bottom")      
           
    def pack_ecosystem(self):
        #Pack species frames and add species buttons
        self.add_species_left_button.pack(side="left")
        for species in self.ecosystem:
            species.pack(side="left",expand=True)
        self.add_species_right_button.pack(side="right")
        
    def unpack_ecosystem(self):
        self.add_species_left_button.pack_forget()
        for species in self.ecosystem:
            species.pack_forget()
        self.add_species_right_button.pack_forget()

    def disable_all_buttons(self):
        """Disable all buttons"""
        self.pass_button.config(state="disabled")
        self.hand.disable()
        self.add_species_left_button.config(state="disabled")
        self.add_species_right_button.config(state="disabled")
        for species in self.ecosystem:
            species.disable()
    
    def enable_all_buttons(self):
        """Disable all buttons"""
        self.pass_button.config(state="normal")
        self.hand.enable()
        self.add_species_left_button.config(state="normal")
        self.add_species_right_button.config(state="normal")
        for species in self.ecosystem:
            species.enable()
        
    def make_payment(self, card):
        #maybe, check payment type and game phase to distinguish how to discard
        # and what to do next
        if self.payment_type is None:
            raise(ValueError)
        if self.payment_type == "food":
            self.game.food_deck.append(card)
            self.pass_player()
            # pass control back to game?
        elif self.payment_type == "discard":
            self.game.discard.append(card)
            # since evolve and feed are "recursive", call set up phase again?
            # or maybe like a make_move(self)
            # if hand is empty, disable_buttons except pass
        else: # it's a reference to the species that called make_payment
            self.payment_type.attach_trait(card)
            # if hand is empty, disable_buttons except pass
        self.payment_type = None
        # for now,
        self.enable_all_buttons()
        self.hand.disable()
        
        # self.setup_phase() #except for feed phase (unless game calls request_payment)
        # if evolve phase, discard or add trait
        # if feed phase, use intelligence (discard)
        # return "control" to player
        
    def request_payment(self, payment_type=None):
        """Make only trait card use buttons active"""
        self.payment_type = payment_type
        self.disable_all_buttons()
        self.hand.enable()
    
    
    def take_turn(self):
        if self.phase == 0: #plant phase
            self.request_payment("food")
        if self.phase == 1:
            self.enable_all_buttons()
            if self.hand.empty.get() is True: # if the hand is empty
                self.pass_player()
            pass
        
    def check_if_can_evolve(self):
        """Check if there are evolve options"""
        # This sounds similar to generate actions
        pass
    
    def setup_phase(self, *args):
        self.phase = self.game.phase.get()
        if self.phase == 0: #plant phase
            self.disable_all_buttons()
            self.hand.enable()
            
        elif self.phase == 1: #evolve phase
            
            self.pass_button.config(state="normal") # you can always pass
  
    def add_species(self, side='R'):
        """Add one species to left or right of the ecosystem"""       
        self.unpack_ecosystem()
        if side == 'L':
            self.ecosystem.insert(0,Species(self))
        elif side == "R":
            self.ecosystem.append(Species(self))
        self.num_species+=1
        self.pack_ecosystem()
        self.request_payment("discard")

    def add_food_to_bag(self):
        """Add food from all species to food bag"""
        self.food_eaten.set(sum([species.food.get() for species in self.ecosystem]))
        
    
    def update_species_frames(self):
        """Update species frames if some have gone extinct?"""
        pass
    
    def pass_player(self):
        """Pass control to the next player and shutdown input"""
        # pass control to next player by asking game who that is
        self.disable_all_buttons()
        self.game.pass_control_next(self)
    
class Human_Player(Player):
    """Player with buttons to modify species and a hand showing"""
    def __init__(self, game, player_index):
        Player.__init__(self, game, player_index)
        self.config(background='yellow')


class AI_Player(Player):
    def __init__(self, *args):
        Player.__init__(self, *args)
#    def __init__(self, game, player_index):
#        Player.__init__(self, game, player_index)
        self.config(background='blue')
        # gonna have to call this everytime a species is added
        # or a trait is added?
        self.disable_all_buttons()  

    def pack_hand(self):
        # Don't Pack hand because humans shouldn't see that
        pass
        
    def add_species(self, side='R'):
        """Add one species to left of the current ecosystem"""       
        #self.disable_all_buttons()  
        Player.add_species(self, side=side)
        

    def make_payment(self, card):
        Player.make_payment(self, card)
        self.disable_all_buttons()  
        
        # self.setup_phase() #except for feed phase (unless game calls request_payment)
        # if evolve phase, discard or add trait
        # if feed phase, use intelligence (discard)
        # return "control" to player
        
    def request_payment(self, payment_type=None):
        """Make only trait card use buttons active"""
        self.payment_type = payment_type

        # choose a card AI        
        self.choose_card_to_discard()
        #self.make_payment(card)

    def choose_card_to_discard(self):
        """Pick a card to discard for payment. 
        Currently, do it randomly since I don't have an AI yet."""
        random.choice(self.hand.card_list).use()
        
    def toggle_eat_me_buttons(self):
        pass
    
    def generate_possible_actions(self):
        # phase dependent 
        # maybe make a tree?
        pass
    
#    def take_turn():
#        pass
    def feed():
        pass
    
    
class Species(tk.Frame):
    MAX_POP = 6    # max population
    MAX_SIZE = 6   # max body size
    def __init__(self, player):
        tk.Frame.__init__(self, player)
        self.player = player # which player owns this species
        self.human = False
        # check if player is human (because human species have active buttons)
        if isinstance(self.player, Human_Player): # better way to do this?
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
        
        
        self.traits = set()          # trait set
        self.trait_index_to_change = None # trait index to update
        self.create_widgets()
        self.grid_widgets()
        
    def create_widgets(self):
        """Create Species widgets"""
        self.feed_button = FeedButton(self, text="FEED")
        self.food_label1 = tk.Label(self, text="Food: ")
        self.food_label2 = tk.Label(self, textvariable=self.food)
        self.eat_button = EatButton(self, text="EAT ME")
        self.add_trait_buttons = []
        self.trait_labels = []
        for t in range(self.player.game.trait_limit):
            self.add_trait_buttons.append(AddTraitButton(self,text="Add Trait",
                                        command=lambda t=t: self.add_trait(t)))
            self.trait_labels.append(tk.Label(self, text="No Trait"))
        self.population_label1 = tk.Label(self, text="Population: ")
        self.population_label2 = tk.Label(self, textvariable=self.population)
        self.body_size_label1 = tk.Label(self, text="Body Size: ")
        self.body_size_label2 = tk.Label(self, textvariable=self.body_size)
        self.add_population_button = AddPopulationButton(self,
                                         text="+1 Population",
                                         command=self.add_population)
        self.add_body_size_button = AddBodySizeButton(self, 
                                        text="+1 Body Size",
                                        command=self.add_body_size)  
                                        
    def grid_widgets(self):
        """Grid Species widgets"""
        self.feed_button.grid(row=0,column=0)           
        self.food_label1.grid(row=0,column=1, sticky='w')   
        self.food_label2.grid(row=0,column=2, sticky='e')   
        self.eat_button.grid(row=0,column=3)         
        for t in range(self.player.game.trait_limit):            
            self.add_trait_buttons[t].grid(row=t+1,column=0)
            self.trait_labels[t].grid(row=t+1,column=1,columnspan=2)       
                                         
        self.population_label1.grid(row=5,column=0)
        self.population_label2.grid(row=5,column=1)
        self.body_size_label1.grid(row=5,column=2)
        self.body_size_label2.grid(row=5,column=3) 
        self.add_population_button.grid(row=6,column=0,columnspan=2)
        self.add_body_size_button.grid(row=6,column=2,columnspan=2)

    def set_food_dependent_flags(self):
        """Set flags depending on how much food is eaten"""
        # check if self.food <= self.population
        # change self.hungry
        pass
    
    def set_population_dependent_flags(self, *args):
        """Set flags depending on how much pop there is"""
        # check if self.food <= self.population
        # change self.hungry
        # change if population can be added (6)
        if self.population.get() == Species.MAX_POP:
            # turn off add population button
            pass
    
    def disable(self):
        """Disable all buttons in this species"""     
        self.feed_button.config(state="disabled")
        self.eat_button.config(state="disabled")    
        for t in range(self.player.game.trait_limit):            
            self.add_trait_buttons[t].config(state="disabled")            
        self.add_population_button.config(state="disabled")
        self.add_body_size_button.config(state="disabled")

    def enable(self):
        """Enable all buttons in this species"""     
        self.feed_button.config(state="normal")
        self.eat_button.config(state="normal")    
        for t in range(self.player.game.trait_limit):            
            self.add_trait_buttons[t].config(state="normal")            
        self.add_population_button.config(state="normal")
        self.add_body_size_button.config(state="normal")
    
    ### NEED A TRAIT HANDLER ###
    # maybe sublass set because different instances of same card does nothing
    # no, for each species, see if traits are in current hand
    # first as long as one card is not in the trait set then you can add trait
    # check for traits added and only allow payment for unique traits
    # order of traits doesn't matter, fill traits until full
    def add_trait(self, t):
        """Add trait to species"""    
        self.trait_index_to_change = t
        self.player.request_payment(self)
        # toggle add button to say delete or something
        
    def attach_trait(self, card):
        self.traits.add(card)
        self.trait_labels[self.trait_index_to_change].config(text=card.name)
        self.trait_index_to_change = None

    
    def add_population(self):
        """Increase population by 1. Assumes this is allowed"""
        # First, check if less than max size
        if self.population.get() >= Species.MAX_POP:
            raise PopulationOverflowException("Cannot add more than 6 population")         
        self.population.set(self.population.get()+1)
        self.player.request_payment("discard")

    def add_body_size(self):
        """Increase body size by 1. Assumes this is allowed"""
        if self.body_size.get() >= Species.MAX_SIZE:
            raise BodySizeOverflowException("Cannot add more than 6 body size")
        self.body_size.set(self.body_size.get()+1)
        self.player.request_payment("discard")
        
    def feed(self):
        """Feed this species from either the watering hole or another species"""
        # or intelligence discard
        pass
    
    def starve(self):
        """Reduce population to fed level"""
        # maybe push condition to caller
        if self.food.get() < self.population.get(): 
            self.population.set(self.food.get())
        if self.population.get() <= 0:
            self.die()
    
    def die(self):
        """Remove species because it starved or was eaten below 1 pop"""
        self.pack_forget()
        self.player.ecosystem.remove(self)
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


game = Evolution(first_player=0)
game.pack(fill="both", expand=True)
game.update()
game.after(5000,game.play_game())
game.mainloop()

#
#def main(): #run mainloop 
#    game = Evolution()
#    game.mainloop()
#
#if __name__ == '__main__':
#    main()