# -*- coding: utf-8 -*-
"""
Sets up and simulates the group stages

@author: @eightyfivepoint
"""

from WorldCupMatch import WorldCupMatch

class WorldCupGroup(object):
    def __init__(self,name,teams):
        self.group_name = name # group name
        self.group_teams = teams # list of group teams
        self.build_group_matches()        
        
    def __repr__(self):
        teams = ""
        for t in self.group_teams:
            teams = teams + t.name + ", "
        return "group %s contains %s" % (self.group_name,teams)        
    
    def build_group_matches(self):
        self.matches = []
        # assume group matches in every group  are in the same order.
        self.matches.append(WorldCupMatch(self.group_teams[0],self.group_teams[1]))
        self.matches.append(WorldCupMatch(self.group_teams[2],self.group_teams[3]))
        self.matches.append(WorldCupMatch(self.group_teams[0],self.group_teams[2]))
        self.matches.append(WorldCupMatch(self.group_teams[1],self.group_teams[3]))
        self.matches.append(WorldCupMatch(self.group_teams[3],self.group_teams[0]))
        self.matches.append(WorldCupMatch(self.group_teams[1],self.group_teams[2]))
    
    def simulate_group_matches(self,simall=False):
        if simall: [m.generate_result('GRP') for m in self.matches]
        else: [m.generate_result('GRP') for m in self.matches if not m.played]
        self.build_table()    
       
    def set_actual_result(self,matchnum,team1_goals,team2_goals):
        # functionality for using the actual result (during the tournament) rather than simulating matches
        self.matches[matchnum].set_group_stats(team1_goals,team2_goals)
        self.matches[matchnum].set_tournament_points('GRP')    

    def build_table(self): 
        # Sort on points, goal dif and then goals scored. Ties on all three not explicitly dealt with, sorry! (they're very rare)
        self.table = sorted(self.group_teams,key = lambda team: (team.points,team.goal_dif,team.goals_for), reverse=True)        
        self.winner = self.table[0]        
        self.runner = self.table[1]        
        
    def print_table(self): # print the group tables
        self.build_table()   
        print "***** GROUP %s Table ******" % self.group_name
        template = "{0:14}{1:3}{2:3}{3:3}{4:3}{5:3}"
        print template.format("Team", " Pl", " GF", " GA", " GD", " Pt") # header
        print '-'*29
        for t in self.table:
            row = [t.group_matches,t.goals_for,t.goals_against,t.goal_dif,t.points]
            print template.format( t.name, *row)
        print '-'*29
            
    def print_matches(self):
        for m in self.matches:
            print m