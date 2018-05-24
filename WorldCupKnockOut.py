# -*- coding: utf-8 -*-
"""
Sets up and simulates the knock-out rounds

@author: @eightyfivepoint
"""

import numpy as np
from WorldCupMatch import WorldCupMatch

class WorldCupKnockOut(object):
    def __init__(self,groups):
        self.groups = groups
        
    def simulate_Round16_matches(self,simall=False):
        if simall: [m.generate_result('R16',penalties=True) for m in self.R16matches]
        else: [m.generate_result('R16',penalties=True) for m in self.R16matches if not m.played] 
        
    def simulate_QF_matches(self,simall=False):
        if simall: [m.generate_result('QF',penalties=True) for m in self.QFmatches]
        else: [m.generate_result('QF',penalties=True) for m in self.QFmatches if not m.played]  
        
    def simulate_SF_matches(self,simall=False):
        if simall: [m.generate_result('SF',penalties=True) for m in self.SFmatches]
        else: [m.generate_result('SF',penalties=True) for m in self.SFmatches if not m.played]          
        
    def simulate_Final(self):
        [m.generate_result('Final',penalties=True) for m in self.Final]
        
    def Round16(self):
        # Set up Round of 16 matches based on groups
        self.R16matches = []
        self.R16teamnames = []
        self.GroupWinners = []
        self.R16matches.append(WorldCupMatch(self.groups[0].winner,self.groups[1].runner)) #1A vs 2B
        self.R16matches.append(WorldCupMatch(self.groups[2].winner,self.groups[3].runner)) #1C vs 2D
        self.R16matches.append(WorldCupMatch(self.groups[1].winner,self.groups[0].runner)) #1B vs 2A
        self.R16matches.append(WorldCupMatch(self.groups[3].winner,self.groups[2].runner)) #1D vs 2C
        self.R16matches.append(WorldCupMatch(self.groups[4].winner,self.groups[5].runner)) #1E vs 2F
        self.R16matches.append(WorldCupMatch(self.groups[6].winner,self.groups[7].runner)) #1G vs 2H
        self.R16matches.append(WorldCupMatch(self.groups[5].winner,self.groups[4].runner)) #1F vs 2E
        self.R16matches.append(WorldCupMatch(self.groups[7].winner,self.groups[6].runner)) #1H vs 2G
        # Record group winners and round of 16 team names (for metrics)
        for group in self.groups:
            self.GroupWinners.append(group.winner.name)
        for m in self.R16matches:
            self.R16teamnames.append(m.team1.name)
            self.R16teamnames.append(m.team2.name)
    
    def ManuallySetRound16(self,R16teams):
        # Manually set Round of 16 matches
        self.R16matches = []
        self.R16teamnames = []
        for i in np.arange(0,15,step=2):
            self.R16matches.append( WorldCupMatch(R16teams[i], R16teams[i+1] ) )
        for m in self.R16matches:
            self.R16teamnames.append(m.team1.name)
            self.R16teamnames.append(m.team2.name)
    
    def QuarterFinal(self):
        # Quarter Final Matches
        self.QFmatches = []
        self.QFteamnames = []
        self.QFmatches.append(WorldCupMatch( self.R16matches[0].winner, self.R16matches[1].winner) ) # 1A/2B vs 1C/2D
        self.QFmatches.append(WorldCupMatch( self.R16matches[2].winner, self.R16matches[3].winner) ) # 1B/2A vs 1D/2C
        self.QFmatches.append(WorldCupMatch( self.R16matches[4].winner, self.R16matches[5].winner) ) # 1E/2F vs 1G/2H
        self.QFmatches.append(WorldCupMatch( self.R16matches[6].winner, self.R16matches[7].winner) ) # 1F/2E vs 1H/2G
        for m in self.QFmatches:
            self.QFteamnames.append(m.team1.name)
            self.QFteamnames.append(m.team2.name)
        
    def SemiFinal(self):
        # Semi final matches
        self.SFmatches = []
        self.SFteamnames = []
        self.SFmatches.append(WorldCupMatch( self.QFmatches[0].winner, self.QFmatches[2].winner) ) # 1A/2B/1C/2D vs 1E/2F/1G/2H
        self.SFmatches.append(WorldCupMatch( self.QFmatches[1].winner, self.QFmatches[3].winner) ) # 1B/2A/1D/2C vs 1F/2E/1H/2G
        for m in self.SFmatches:
            self.SFteamnames.append(m.team1.name)
            self.SFteamnames.append(m.team2.name)
    
    def Final(self):
        # Final
        self.Final = [WorldCupMatch( self.SFmatches[0].winner, self.SFmatches[1].winner)]
        self.Finalteamnames = [self.Final[0].team1.name, self.Final[0].team2.name]
    
        
    def print_matches(self,matches):
        print "***** KNOCKOUT GAMES ******"
        for m in matches:
            if m.played:
                if m.penalties:
                    print m.__repr__() + " --->  %s wins on penalties." % (m.winner.name)
                else:
                    print m.__repr__() + " --->  %s wins." % (m.winner.name)
            else:
                print m 
