# -*- coding: utf-8 -*-
"""
Simulates the entire tournament once.

@author: @eightyfivepoint
"""

from WorldCupGroup import WorldCupGroup
from WorldCupKnockOut import WorldCupKnockOut

class WorldCupSim(object):
    def __init__(self,group_names,teams,verbose):
        self.group_names = group_names
        self.teams = teams
        self.groups = []
        self.verbose = verbose
        
    def runsim(self):
        # Run full World Cup Sim
        # Put teams in groups
        for g in self.group_names:
            group_teams = [t for t in self.teams if t.group==g]
            self.groups.append(WorldCupGroup(g,group_teams))
        # Simulation group matches
        for g in self.groups:
            g.simulate_group_matches()
            if self.verbose:
                g.print_matches()
                g.print_table()
        # BUild knock-out stage of tournament
        self.KnockOut = WorldCupKnockOut(self.groups)
        # ROUND OF 16
        self.KnockOut.Round16()
        self.KnockOut.simulate_Round16_matches()
        if self.verbose:        
            self.KnockOut.print_matches(self.KnockOut.R16matches)
        # Quarter Finals
        self.KnockOut.QuarterFinal()
        self.KnockOut.simulate_QF_matches()
        if self.verbose:
            self.KnockOut.print_matches(self.KnockOut.QFmatches)
        # Semi Finals
        self.KnockOut.SemiFinal()
        self.KnockOut.simulate_SF_matches()
        if self.verbose:        
            self.KnockOut.print_matches(self.KnockOut.SFmatches)
        # Final
        self.KnockOut.Final()
        self.KnockOut.simulate_Final()
        if self.verbose:
            self.KnockOut.print_matches(self.KnockOut.Final)
            
