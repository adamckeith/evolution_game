# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 00:29:25 2017

@author: ACKWinDesk
"""
import tkinter as tk

class PlayerButton(tk.button):
    # pass player, add species
    pass

class SpeciesButton(tk.button):
    # + pop, body size, feed, add trait, eat
    pass

class PlantPhaseButton(tk.button):
    # trait use    
    pass

class EvolvePhaseButton(tk.button):
    #pass, add species, +pop,bodysize, add trait, trait use
    pass

class FeedPhaseButton(tk.button):
    # feed, eat, pass?
    pass

class TraitUseButton(PlantPhaseButton, EvolvePhaseButton, FeedPhaseButton):
    # feed phase because of intelligence
    pass

class AddTraitButton(EvolvePhaseButton, SpeciesButton):
    # switch to remove trait when trait added
    # when trait removed, switch back behavior
    pass

class AddPopulationButton(EvolvePhaseButton, SpeciesButton):
    pass

class AddBodySizeButton(EvolvePhaseButton, SpeciesButton):
    pass

class FeedButton(FeedPhaseButton, SpeciesButton):
    pass

class EatButton(FeedPhaseButton, SpeciesButton):
    pass

class PassButton(EvolvePhaseButton, FeedPhaseButton, PlayerButton):
    # feed phase because of fat tissue
    pass