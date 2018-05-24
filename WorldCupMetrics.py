# -*- coding: utf-8 -*-
"""
A collection of (poorly-commented) plotting and output routines

@author: @eightyfivepoint
"""

import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

def SetShortNames():
    # For plot axis labels
    ShortNames = {
        'Russia':'RUS',
        'Uruguay':'URU',
        'Egypt':'EGP',
        'Saudi Arabia':'SAU',
        'Portugal':'POR',
        'Spain':'SPA',
        'Iran':'IRA',
        'Morocco':'MOR',
        'France':'FRA',
        'Peru':'PER',
        'Denmark':'DEN',
        'Australia':'AUS',
        'Argentina':'ARG',
        'Croatia':'CRO',
        'Iceland':'ICE',
        'Nigeria':'NIG',
        'Brazil':'BRA',
        'Switzerland':'SWI',
        'Costa Rica':'COS',
        'Serbia':'SER',
        'Germany':'GER',
        'Mexico':'MEX',
        'Sweden':'SWE',
        'Korea Republic':'KOR',
        'South Korea':'KOR',
        'Belgium':'BEL',
        'England':'ENG',
        'Tunisia':'TUN',
        'Panama':'PAN',
        'Poland':'POL',
        'Colombia':'COL',
        'Senegal':'SEN',
        'Japan':'JAP'
    }
    return ShortNames

def SimWinners(sims,teamnames,includeOdds=False, randsims=None, save=True):
    # Probability of top-16 favourites each winning tournament
    ShortNames = SetShortNames()
    nTeamsPlot = 16 # number of teams to plot
    Nsims = len(sims)
    Winners = [x.KnockOut.Final[0].winner.name for x in sims]
    WinnerFreq = [(name,Winners.count(name)) for name in teamnames]
    WinnerFreq = sorted( WinnerFreq, key = lambda x : x[1], reverse=True)
    WinnerFreq = [(n,c) for (n,c) in WinnerFreq if c > 0]
    WinnerFreq = WinnerFreq[0:nTeamsPlot]
    WinnerNames = [x[0] for x in WinnerFreq]
    fig, ax = plt.subplots(figsize=(10, 5))   
    ind = np.arange(len(WinnerFreq))
    width = 0.6
    WinnerProp = np.array([x[1] for x in WinnerFreq],'float')/float(Nsims)
    ax.bar(ind+(1-width)/2., 100.*WinnerProp, width=width, color='r', linewidth=0, alpha = 0.3,label='Simulations') 
    ax.set_ylabel('Prob of Winning Tournament (%)',fontsize=12)
    ax.set_xticks(ind + 0.5)
    ax.set_xticklabels([ShortNames[name] for name in WinnerNames],fontsize=12)
    ax.set_xlim(0,nTeamsPlot)
    ax.yaxis.grid()
    #ax.legend(loc='best',framealpha=0.2,frameon=False,fontsize=12, numpoints=1)
    #ax.get_xticklabels().set_fontsize(20)
    fig.suptitle("WC2018 Favourites",fontsize=14)
    if save:
        figname = 'SimWinners.png'
        plt.savefig(figname,dpi=400,bbox_inches='tight',pad_inches=0.1) 
    
    
def SimFinalists(sims,teamnames,ShortNames):
   # Find most frequent finalists
   Finalists = [(x.KnockOut.Final[0].team1.name,x.KnockOut.Final[0].team2.name) for x in sims]
   F = [(x[0],x[1],Finalists.count(x)) for x in Finalists]
   F = sorted( F, key = lambda x : x[2], reverse=True)
   # get uniques
   FinalistFreq = []
   for f in F:
       if f not in FinalistFreq:
           FinalistFreq.append(f)
   print FinalistFreq

def TraceTeam(sims,teamname, verbose=False):
    # trace probability of a team progressing through the tournament
    Progress = []
    Nsims = float(len(sims))
    stages = ['GRP','R16','QF','SF','Final','Winner']
    for s in sims:
        p = 0
        if teamname in s.KnockOut.R16teamnames: p += 1
        if teamname in s.KnockOut.QFteamnames: p += 1
        if teamname in s.KnockOut.SFteamnames: p += 1
        if teamname in s.KnockOut.Finalteamnames: p += 1
        if teamname == s.KnockOut.Final[0].winner.name: p += 1
        Progress.append(stages[p])    
    ProgressFreq = [Progress.count(s)/Nsims for s in stages]
    assert np.isclose( np.sum(ProgressFreq),1.,atol=0.001,rtol=0.0)
    ProgressFreq = 1-np.cumsum(ProgressFreq)
    Progress = (teamname,ProgressFreq[0],ProgressFreq[1],ProgressFreq[2],ProgressFreq[3],ProgressFreq[4]) 
    if verbose:
        print "%s: %1.2f,%1.2f,%1.2f,%1.2f,%1.2f" % Progress
    return Progress


def ExpectedGroupFinishes(sims,group_names, group_name):
    # Probability of each team in a group finishing in each position
    Nsims = len(sims)
    ind = group_names.index(group_name)
    Teams = sims[0].groups[ind].group_teams
    Table = {}
    for team in Teams:
        Table[team.name] = np.zeros(4)
    for i in range(0,Nsims):
        sims[i].groups[ind].build_table
        for t,p in zip(sims[i].groups[ind].table,range(0,4)):
            Table[t.name][p] += 1
    n = float(Nsims)
    Table = [(t,Table[t][0]/n,Table[t][1]/n,Table[t][2]/n,Table[t][3]/n) for t in Table.keys()]
    Table = sorted(Table,key = lambda x: x[1]+x[2],reverse=True)
    return Table
    
def ExpectedGroupFinishesPlot(sims,group_names,save=True):
    # Make group table probability plot
    Tables = [ExpectedGroupFinishes(sims,group_names,group) for group in group_names]
    fig,axes = plt.subplots(nrows=4,ncols=2,figsize=(10, 9))
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=0.45, hspace=0.4)
    nGroupTeams = 4
    for Table,ax,group in zip(Tables,axes.flatten(),group_names):
        grid = np.zeros((nGroupTeams,nGroupTeams),dtype=float)
        gridmax = 0.8
        gridmin = 0
        for i in range(nGroupTeams):
            for j in range(nGroupTeams):
                grid[i,j] = np.round( Table[i][j+1] ,3)
                if grid[i,j] <0.01:
                    grid[i,j] = gridmin
        Y = np.arange(nGroupTeams+0.5, 0, -1)
        X = np.arange(0.5, nGroupTeams+1, 1)
        X, Y = np.meshgrid(X, Y)
        cmap = plt.get_cmap('Blues')#cool, Reds, Purples
        levels = MaxNLocator(nbins=gridmax/0.01).tick_values(gridmin,gridmax)# grid.max())
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        im = ax.pcolormesh(X, Y, grid,cmap=cmap,norm=norm)
        ax.set_xlim(0.5,nGroupTeams+0.5)
        ax.set_ylim(0.5,nGroupTeams+0.5)
        teams = [t[0] for t in Table]
        for i in range(nGroupTeams): 
            if teams[i]=='Korea Republic' or teams[i]=='South Korea':
                teams[i] = 'S. Korea'
        ax.set_yticks(np.arange(1,nGroupTeams+1,1))
        ax.set_xticks(np.arange(1,nGroupTeams+1,1))
        ax.set_yticklabels(teams[::-1],color='r',fontsize=11)
        ax.set_xticklabels( ['1st', '2nd', '3rd', '4th'], color='k', fontsize=11 )
        ax.tick_params(axis=u'both', which=u'both',length=0)
        ax.set_title("Group " + group,color='r')
        pthresh=0.01
        Qual = np.array( np.round(100*np.sum( grid[:,:2], axis=1 ),0), dtype=int)
        for i in range(nGroupTeams):
            for j in range(nGroupTeams):
                if grid[i,j]>=pthresh:
                    s = "%1.0d" % (round(100*grid[i,j],0))
                    ax.text(j+0.9,nGroupTeams-i-0.15,s,fontsize=10,color='k')
        fig.set_facecolor('0.95')
        # twin axis
        ax2 = ax.twinx()
        ax2.set_ylim((0.5,0.5 + nGroupTeams ))
        ax2.set_yticks(np.arange(1,nGroupTeams+1,1))
        ax2.set_yticklabels( Qual[::-1] ,color='k')
        ax2.text(3.55+0.9,nGroupTeams+0.65,'Qual',fontsize=11,color='k')
        ax2.tick_params(axis=u'both', which=u'both',length=0)
    if save:
        figname = 'ExpectedGroupFinishes.png'
        plt.savefig(figname,dpi=400,bbox_inches='tight',pad_inches=0.1) 
        

def ExpectedGroupResults(sims,group_names, group_name):
    # Find most frequent results in group stage
    Nsims = len(sims)
    ind = group_names.index(group_name)
    resultslist = np.zeros( (Nsims,6),dtype = 'int')
    for i in range(0,Nsims):
        resultslist[i,:] = [100*m.team1_goals+m.team2_goals for m in sims[i].groups[ind].matches]
    most_freq = [ (int(x/100),int(x % 100)) for x in mode(resultslist)[0][0] ]
    # NOW PRINT RESULTS
    print " GROUP %s RESULTS " % (group_name)
    for i in range(len(most_freq)):
        team1 = sims[0].groups[ind].matches[i].team1.name
        team2 = sims[0].groups[ind].matches[i].team2.name
        print "%s %s v %s %s" % (team1,most_freq[i][0],most_freq[i][1],team2)

def ExpectedKnockOutResults(sims,stage,Nmatches):
    # Find most frequent results in each knock-out match
    Nsims = float(len(sims))
    matches = 's.KnockOut.' + stage
    print matches     
    for i in range(Nmatches):
        resultslist = []
        for s in sims:
            m = eval(matches)
            resultslist.append((m[i].team1.name,m[i].team1_goals,m[i].team2.name,m[i].team2_goals))
        R = [(r[0],r[1],r[2],r[3],resultslist.count(r)/Nsims) for r in resultslist]
        R = sorted(R,key = lambda x: x[4], reverse=True)
        # get uniques
        ResultsFreq = []
        for r in R:
            if r not in ResultsFreq:
                ResultsFreq.append(r)
        # NOW PRINT RESULTS
        print " KNOCKOUT RESULTS " 
        for r in ResultsFreq[0:3]:
            print "%s,%s,%s,%s,%s" % r


def makeProgressPlot( sims, teamnames, save=True ):
    # Probability of each team making it to each successive stage of the tournamnet
    ProgressArray = []
    for t in teamnames:
        ProgressArray.append( TraceTeam(sims,t) )
    nRounds = 5
    nteams = len( ProgressArray )
    ProgressArray = sorted( ProgressArray, key = lambda x: np.sum(x[1:]), reverse=True )
    grid = np.zeros((nteams,nRounds),dtype=float)
    gridmax = 0.9
    gridmin = 0
    for i in range(nteams):
        for j in range(nRounds):
            grid[i,j] = np.round( ProgressArray[i][j+1] ,3)
            if grid[i,j] <0.01:
                grid[i,j] = gridmin

    fig,axes = plt.subplots(nrows=1,ncols=2,figsize=(10, 6))   
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=0.45)

    teams = [t[0] for t in ProgressArray]
    for i in range(nteams): 
        if teams[i]=='Korea Republic':
            teams[i] = 'South Korea'

    nteams = nteams/2

    for sp,ax in zip([0,1],axes):
        subgrid = grid[sp*nteams:(sp+1)*nteams,:]
        subteams = teams[sp*nteams:(sp+1)*nteams]
        Y = np.arange(nteams+0.5, 0, -1)
        X = np.arange(0.5, nRounds+1, 1)
        X, Y = np.meshgrid(X, Y)
        
        cmap = plt.get_cmap('Blues')#cool, Reds, Purples
        levels = MaxNLocator(nbins=gridmax/0.01).tick_values(gridmin,gridmax)# grid.max())
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        ax.pcolormesh(X, Y, subgrid,cmap=cmap,norm=norm)
        ax.set_xlim(0.5,nRounds+0.5)
        ax.set_ylim(0.5,nteams+0.5)

        ax.set_yticks(np.arange(1,nteams+1,1))
        ax.set_xticks(np.arange(1,nRounds+1,1))
        ax.set_yticklabels(subteams[::-1],color='r',fontsize=11)
        ax.set_xticklabels( ['R16', 'QF', 'SF', 'F', 'W'], color='k', fontsize=12 )
        pthresh=0.01
        for i in range(nteams):
            for j in range(nRounds):
                if subgrid[i,j]>=pthresh:
                    s = "%1.0d" % (round(100*subgrid[i,j],0))
                    ax.text(j+0.9,nteams-i-0.1,s,fontsize=9,color='k')
                else:
                    ax.text(j+0.9,nteams-i-0.1,"<1",fontsize=9,color='k')
        fig.set_facecolor('0.95')
        ax2 = ax.twiny()
        ax2.set_xlim(0.5,nRounds+0.5)
        ax2.set_xticks(np.arange(1,nRounds+1,1))
        ax2.set_xticklabels( ['R16', 'QF', 'SF', 'F', 'W'], color='k' , fontsize=12 )
        ax.tick_params(axis='y',which='both',left='off',right='off')
        ax.tick_params(axis='x',which='both',top='off',bottom='off')
        ax2.tick_params(axis='x',which='both',top='off',bottom='off')
    fig.suptitle('WC2018: Probability of reaching round (%)',y=1.0,fontsize=14)
    if save:
        figname = 'ExpectedProgress.png'
        plt.savefig(figname,dpi=400,bbox_inches='tight',pad_inches=0.1)     
  
def simstats(sims): 
    # print some useful tournament stats
    print "Interesting simulation stats:"
    Favourites = ['Germany','Brazil','Spain','France','Argentina','Portugal','Belgium','Colombia','England','Uruguay']
    prev_winners = ['Germany', 'Brazil', 'Spain', 'France', 'Uruguay', 'Argentina', 'England']
    African = ['Egypt','Morocco','Nigeria','Senegal','Tunisia']
    SouthCentral = ['Brazil','Peru','Uruguay','Argentina','Mexico','Costa Rica','Panama','Colombia']
    Europe = ['Belgium','Serbia','England','France','Spain','Germany','Switzerland','Portugal','Sweden','Denmark','Poland','Croatia','Iceland']
    Australasia = ['Iran','Saudi Arabia','Russia','Australia','Japan','South Korea']
    All = African + SouthCentral + Europe + Australasia
    p = 0
    nsims = float(len(sims))
    for s in sims:
        if s.KnockOut.Final[0].winner.name not in prev_winners:
            p+=1
    print "New winners = %1.3f" % (p/nsims)
    p = 0
    for s in sims:
        if s.KnockOut.Final[0].winner.name  in All:
            p+=1
    assert p==nsims
    p = 0
    for s in sims:
        if s.KnockOut.Final[0].winner.name  in Europe:
            p+=1
    print "Europe winners = %1.3f" % (p/nsims)
    p = 0
    for s in sims:
        if s.KnockOut.Final[0].winner.name  in African:
            p+=1
    print "African winners = %1.3f" % (p/nsims)
    p = 0
    for s in sims:
        if s.KnockOut.Final[0].winner.name  in Australasia:
            p+=1
    print "Australasia winners = %1.3f" % (p/nsims)
    p = 0
    for s in sims:
        if s.KnockOut.Final[0].winner.name  in SouthCentral:
            p+=1
    print "South Central American winners = %1.3f" % (p/nsims)
    p = 0   
    for s in sims:
        if s.KnockOut.groups[6].winner.name not in ['England', 'Belgium'] or s.KnockOut.groups[6].runner.name not in ['England', 'Belgium']:
            p+=1
    print "England or Beglium not qualify: %1.3f" % (p/nsims)
    p = 0
    for s in sims:
        if s.KnockOut.groups[7].winner.name in ['Japan', 'Senegal'] or s.KnockOut.groups[7].runner.name in ['Japan', 'Senegal']:
            p+=1
    print "Senegal or Japan qualify: %1.3f" % (p/nsims)
    p = 0
    for s in sims:
        if (s.KnockOut.R16matches[4].team1.name=='Brazil' and s.KnockOut.R16matches[4].team2.name=='Germany') or (s.KnockOut.R16matches[6].team1.name=='Germany' and s.KnockOut.R16matches[6].team2.name=='Brazil'):
            p+=1
    print "Brazil & Germany meet in R16: %1.3f" % (p/nsims)
    p = 0
    for s in sims:
        if (s.KnockOut.SFteamnames[0] not in Favourites) or (s.KnockOut.SFteamnames[1] not in Favourites) or (s.KnockOut.SFteamnames[2] not in Favourites) or (s.KnockOut.SFteamnames[3] not in Favourites):
            p+=1
    print "non-favourite makes semi-final: %1.3f" % (p/nsims)
