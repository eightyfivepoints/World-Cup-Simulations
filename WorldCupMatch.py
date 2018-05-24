# -*- coding: utf-8 -*-
"""
World Cup match class. Simulates the individual matches.

@author: @eightyfivepoint
"""

import scipy as scipy
import scipy.stats
import numpy as np

class WorldCupMatch(object):
    def __init__(self,team1,team2):
        self.played = False
        self.penalties = False
        self.team1 = team1
        self.team2 = team2
        self.eloK = 60 # for world cup (see http://www.eloratings.net/about)
        self.run_hot = True
        self.elo_only_model()
        
    def __repr__(self):
        if self.played:
            return "Match %s %s vs %s %s" % (self.team1.name, self.team1_goals, self.team2_goals, self.team2.name)
        else:
            return "Match %s vs %s." % (self.team1.name, self.team2.name)
        
    def elo_only_model(self):
        # log( mu ) = const + xe*(elo_diff/100) + eloHA*IsHost?
        self.const = 0.1557
        self.xe = 0.169 # coeff elo_diff / 100
        self.eloHA = 0.182/self.xe*100 # get regression coefficient in units of elo difference
        self.model = "Elo"
            
    def set_group_stats(self,team1_goals, team2_goals, stage):
        # update 
        self.played = True
        if stage=='GRP':
            self.team1.group_matches += 1
            self.team2.group_matches += 1
        self.team1.total_matches += 1
        self.team2.total_matches += 1
        self.team1_goals = team1_goals
        self.team2_goals = team2_goals
        self.team1.goals_for += team1_goals
        self.team1.goals_against += team2_goals
        self.team2.goals_for += team2_goals
        self.team2.goals_against += team1_goals       
        self.team1.goal_dif = self.team1.goals_for - self.team1.goals_against
        self.team2.goal_dif = self.team2.goals_for - self.team2.goals_against   
        if self.team1_goals > self.team2_goals:
            self.winner = self.team1
            if stage=='GRP':
                self.team1.points += 3                        
        elif self.team1_goals < self.team2_goals:
            self.winner = self.team2            
            if stage=='GRP':
                self.team2.points += 3
        else:
            if stage=='GRP':
                self.team1.points += 1
                self.team2.points += 1
     
    
    def generate_result(self,stage,penalties=False,verbose=False):
        # Does one team have home advantage (i.e. the host)?
        if self.team1.host:
            HA = self.eloHA
        elif self.team2.host:
            HA = -self.eloHA
        else:
            HA = 0.0
        assert not (self.team1.host and self.team2.host)
        # Elo differences, including home advantage effect
        elo_diff = self.team1.elorank - self.team2.elorank + HA
        # Select model & calculated Poisson means
        if self.model=="Elo": 
            mu1 = float(np.exp( self.const + elo_diff*self.xe/100 ))
            mu2 = float(np.exp( self.const - elo_diff*self.xe/100 ))
        # Draw goals from Poisson distribution
        team1_goals = int(scipy.stats.poisson.rvs(mu1,size=1))
        team2_goals = int(scipy.stats.poisson.rvs(mu2,size=1))
        if verbose:
            print "%s %d vs %d %s" % (self.team1.name, team1_goals, team2_goals, self.team2.name)
            print "Mus: %1.1f, %1.1f" % (mu1,mu2)
            print "Elos: %1.1f, %1.1f" % (self.team1.elorank,self.team2.elorank)
        # Update group stats
        self.set_group_stats(team1_goals,team2_goals,stage)
        # Simulate penalty shoot-out if necessary
        if penalties and team1_goals==team2_goals: 
            self.penalty_shootout()
        # Finally, update elo score for each team if running 'hot'
        if self.run_hot:
            self.update_elo_scores_ELORATING( team1_goals-team2_goals, elo_diff)
        if verbose:
            print "Elos: %1.1f, %1.1f" % (self.team1.elorank,self.team2.elorank)


    def update_elo_scores_ELORATING(self, goal_diff, elo_diff):
        # see http://www.eloratings.net/about
        if np.abs( goal_diff ) == 2:
            K = self.eloK * 1.5
        elif np.abs( goal_diff ) > 2:
            K = self.eloK * (1.75 + ( np.abs( goal_diff ) - 3 ) / 8. )
        else:
            K = self.eloK
        W = 1. if goal_diff>0 else 0. if goal_diff<0 else 0.5
        We = 1. / ( 10**(-1.*elo_diff/400.) + 1. )        
        self.team1.elorank += K * (W-We)
        self.team2.elorank += K * (We-W)


    def penalty_shootout(self, Ninit = 5):
        # generate 5 penalties each and check against skill
        self.penalties = True
        team1_success = np.sum(np.random.uniform(size=Ninit)<=self.team1.penaltyskill)
        team2_success = np.sum(np.random.uniform(size=Ninit)<=self.team2.penaltyskill)
        if team1_success > team2_success:
            self.winner = self.team1
        elif team1_success < team2_success:
            self.winner = self.team2
        else: # determine winner based on relative penalty strenghts
            high = self.team1.penaltyskill + self.team2.penaltyskill
            if np.random.uniform(size=1,high=high)<self.team1.penaltyskill:
                self.winner = self.team1
            else:
                self.winner = self.team2


    
    
