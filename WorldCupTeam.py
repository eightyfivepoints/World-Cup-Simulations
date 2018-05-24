# -*- coding: utf-8 -*-
"""
World Cup team class

@author: @eightyfivepoint
"""

class WorldCupTeam(object):
    def __init__(self,group,name,elo,seed,penaltyskill,distance,hostname):
        self.name = name # Country
        self.group = group
        self.elorank = elo
        self.seed = seed
        self.penaltyskill = penaltyskill
        self.hometeam = name=='Russia'
        self.group_matches = 0
        self.total_matches = 0
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.host = self.name == hostname
        self.dist_to_host = distance  # not used
              
        
    def __repr__(self):
        return "%s, %s, %s" % (self.name,self.group,self.elorank)