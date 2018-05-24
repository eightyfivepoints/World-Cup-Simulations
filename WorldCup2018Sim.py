# -*- coding: utf-8 -*-
"""
Main script for running world cup simulations

@author: @eightyfivepoint
"""

import numpy as np
from WorldCupTeam import WorldCupTeam
from WorldCupSim import WorldCupSim
import WorldCupMetrics as met
import copy as copy
import pandas as pd

def get_WorldCup2018_data():
    teamdata = pd.read_csv('WorldCup2018_groups.csv')
    return teamdata
                    
# ************ Simulations Parameters ***************
hostname = 'Russia'
Nsims = 1000 # number of tournament simulations to run
verbose = True # set to true to print outcome of all matches and group tables in each sim iteration
savePlots = True # plots saved in same directory

# ************ Sim Set-up ***************
print "loading data"
teamdata = get_WorldCup2018_data()
group_names = sorted(np.unique(teamdata['Group']))
teamnames = list( teamdata['Country'].values )
sims = []

# ************ MAIN SIMULATIONS LOOP ***************
print "starting sims: 0 sims done"
for i in range(0,Nsims):
    # collect team data (needs to be redone in each loop of sim)
    teams = []
    for ix,row in teamdata.iterrows():
        teams.append( WorldCupTeam( row['Group'],row['Country'],row['Elo_lag'],row['Seed'],row['PenaltySkill'],row['Dist_to_Moscow'],hostname) )

    # initialise simulation
    s = WorldCupSim(group_names,teams,verbose=verbose)
    
    # run simulated world cup
    s.runsim() 
    sims.append(copy.deepcopy(s))

    if i>0 and i % 1000 == 0: 
        print "               %s sims done" % (i)

# ************ Plots & Statistics ***************
print "generating plots and statistics"
met.SimWinners(sims,teamnames,includeOdds=False, save=savePlots)
met.makeProgressPlot( sims, teamnames, save=savePlots )
met.ExpectedGroupFinishesPlot(sims,group_names, save=savePlots)

# Print some interesting tournament predictions
met.simstats(sims)

print "done"

## ************  USEFUL INFO ************  ##

### to print tables for the jth group in the ith simulations 
#i=0 # 0->Nsims-1
#j=0 # group indices go from 0->7
#print sims[i].groups[j].print_table() 

### to print group matches 
#sims[i].groups[j].print_matches()

### to print results for a given KO round of the tournament 
#sims[i].KnockOut.print_matches(sims[i].KnockOut.R16matches)
#sims[i].KnockOut.print_matches(sims[i].KnockOut.QFmatches)
#sims[i].KnockOut.print_matches(sims[i].KnockOut.SFmatches)
#sims[i].KnockOut.print_matches(sims[i].KnockOut.Final)
        
### Print the most frequent results in each knock-out round
#met.ExpectedKnockOutResults(sims,'R16matches',8)
#met.ExpectedKnockOutResults(sims,'QFmatches',4)
#met.ExpectedKnockOutResults(sims,'SFmatches',2)
#met.ExpectedKnockOutResults(sims,'Final',1)