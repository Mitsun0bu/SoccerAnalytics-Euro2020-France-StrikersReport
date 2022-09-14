import math

import matplotlib.pyplot as plt

from   mplsoccer  import Sbopen, Pitch
from   statistics import mean


##### FUNCTION DEFINITIONS #####

def getGameIDList(dfMatch, teamName):
    '''
    Parameters :
        dfMatch  : DataFrame
        teamName : string

    Returns    :
        A list of IDs for the games played by a team during a given competition
    '''

    gameList = []
    for matchID, homeTeam, awayTeam in dfMatch[['match_id','home_team_name', 'away_team_name']].itertuples(index=False):
        if (homeTeam == teamName or awayTeam == teamName):
            gameList.append(matchID)

    return gameList

def getOpponentList(dfMatch, teamName):
    '''
    Parameters :
        dfMatch  : DataFrame
        teamName : string

    Returns    :
        A list of IDs for the games played by a team during a given competition
    '''

    opponentList = []
    for homeTeam, awayTeam in dfMatch[['home_team_name', 'away_team_name']].itertuples(index=False):
        if   homeTeam == teamName :
            opponentList.append(awayTeam)
        elif awayTeam == teamName:
            opponentList.append(homeTeam)
    return opponentList

def getPlayerAverageXg(dfMatch, teamGameList, playerName):
    '''
    Parameters :
        dfMatch      : DataFrame
        teamGameList : list
        playerName   : string

    Returns    :
        The average xG value for a given player during a given competition
    '''
    
    xgList = []
    for i in teamGameList:
        for matchID in dfMatch['match_id']:
            if matchID == i:
                dfEvent = parser.event(matchID)[0]
                for  pName, xgValue in dfEvent[['player_name','shot_statsbomb_xg']].itertuples(index=False):
                    if (math.isnan(xgValue) is False and
                        pName == playerName):
                            xgList.append(xgValue)
            else:
                continue
            
    averageXg = mean(xgList)

    return averageXg

def getPlayerShotsNumber(dfMatch, teamGameList, playerName):
    '''
    Parameters :
        dfMatch      : DataFrame
        teamGameList : list
        playerName   : string

    Returns    :
        The number of shots taken by a given player during a given competition
    '''
    
    nShot = 0
    for i in teamGameList:
        for matchID in dfMatch['match_id']:
            if matchID == i:
                dfEvent = parser.event(matchID)[0]
                for  pName, t in dfEvent[['player_name','type_name']].itertuples(index=False):
                    if (pName == playerName and t == 'Shot'):
                            nShot += 1
    return nShot

def getPlayerGoalsNumber(dfMatch, teamGameList, playerName):
    '''
    Parameters :
        dfMatch      : DataFrame
        teamGameList : list
        playerName   : string

    Returns    :
        The number of goals scored by a given player during a given competition
    '''
    
    nGoal = 0
    for i in teamGameList:
        for matchID in dfMatch['match_id']:
            if matchID == i:
                dfEvent = parser.event(matchID)[0]
                for  pName, outcome in dfEvent[['player_name','outcome_name']].itertuples(index=False):
                    if (pName == playerName and outcome == 'Goal'):
                            nGoal += 1
    return nGoal

def getCompetitionAverageXg(dfMatch):
    '''
    Parameters :
        dfMatch : DataFrame

    Returns    :
        The average xG value during a given competition
    '''

    xgList = []
    for matchID in dfMatch['match_id']:
        dfEvent = parser.event(matchID)[0]
        for  pName, xgValue in dfEvent[['player_name','shot_statsbomb_xg']].itertuples(index=False):
            if (math.isnan(xgValue) is False):
                xgList.append(xgValue)
            
    averageXg = mean(xgList)

    return averageXg

def getCompetitionShotsNumber(dfMatch):
    '''
    Parameters :
        dfMatch      : DataFrame

    Returns    :
        The number of shots taken during a given competition
    '''
    
    nShot = 0
    for matchID in dfMatch['match_id']:
        dfEvent = parser.event(matchID)[0]
        for pName, t in dfEvent[['player_name', 'type_name']].itertuples(index=False):
            if (t == 'Shot'):
                nShot += 1
    return nShot

def getCompetitionGoalsNumber(dfMatch):
    '''
    Parameters :
        dfMatch      : DataFrame

    Returns    :
        The number of goals scored during a given competition
    '''
    
    nGoal = 0
    for matchID in dfMatch['match_id']:
        dfEvent = parser.event(matchID)[0]
        for pName, outcome in dfEvent[['player_name', 'outcome_name']].itertuples(index=False):
            if (outcome == 'Goal'):
                nGoal += 1
    return nGoal

def getMatchPasses(dfMatch, matchID):
    '''
    Parameters :
        dfMatch : DataFrame
        matchID : int

    Returns     :
        A dataframe containing all the passes that occured during a given match
    '''

    for match in dfMatch:
        dfEvents    = parser.event(matchID)[0]
        matchPasses = dfEvents.loc[(
                                   (dfEvents['type_name']     == 'Pass')   &
                                   (dfEvents['sub_type_name'] != 'Throw-in')
                                   )]
    return matchPasses

def getMatchShots(dfMatch, matchID):
    '''
    Parameters :
        dfMatch : DataFrame
        matchID : int

    Returns     :
        A dataframe containing all the shots that occured during a given match
    '''

    for match in dfMatch:
        dfEvents   = parser.event(matchID)[0]
        matchShots = dfEvents.loc[((dfEvents['type_name'] == 'Shot'))].set_index('id')

    return matchShots

def getKeyPassIndexList(dfMatch, matchID):
    '''
    Parameters :
        dfMatch : DataFram
        matchID : int

    Returns    :
        A list containing ID of key passes that occured in a given match
    '''
    
    indexList       = []
    typeNameList    = []
    dfEvent = parser.event(matchID)[0]
    for index, typeName, subTypeName in dfEvent[['index', 'type_name', 'sub_type_name']].itertuples(index=False):
        if subTypeName != 'Throw-in':
            indexList.append(index)
            typeNameList.append(typeName)

    # myList = list(zip(indexList, typeNameList))
    
    keyPassIndexList  = []
    for i in range(0, len(typeNameList)):
        if (
                (typeNameList[i] == 'Pass')    and 
                (i + 1 < len(typeNameList) - 1 and typeNameList[i + 1] != 'Pass')
           ):
            if (
                (i + 1 < len(typeNameList) - 1 and typeNameList[i + 1] == 'Shot') or
                (i + 2 < len(typeNameList) - 1 and typeNameList[i + 2] == 'Shot') or
                (i + 3 < len(typeNameList) - 1 and typeNameList[i + 3] == 'Shot') or
                (i + 4 < len(typeNameList) - 1 and typeNameList[i + 4] == 'Shot') or
                (i + 5 < len(typeNameList) - 1 and typeNameList[i + 5] == 'Shot')
                ):
                keyPassIndexList.append(indexList[i])

    return keyPassIndexList

def drawPlayerPasses(matchPasses, keyPassIndexList, teamID, playerName):
    ''' 
    Parameters :
        matchPasses      : DataFrame
        keyPassIndexList : list
        teamID           : int
        playerName       : string

    Returns    :
        A pitch with arrows representing 
        the passes (blue) and the key passes (red) 
        from a given player, during a given match.
    '''

    # Draw the pitch
    pitch   = Pitch(line_color = "black", linewidth = 3)
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plot the passes on the pitch
    oppositeTeam = ""
    for i, p in matchPasses.iterrows():
        if p['player_name'] == playerName:
            # Plot circles
            x          = p['x']
            y          = p['y']
            passCircle = plt.Circle((x, y), 1, color="blue")
            passCircle.set_alpha(.2)
            ax.add_patch(passCircle)
            
            # Plot arrows
            dx         = p['end_x'] - x
            dy         = p['end_y'] - y
            
            # Determine arrow color
            for idx in keyPassIndexList:
                if p['index'] == idx:
                    arrowWidth = 5
                    arrowColor = "crimson"
                    break
                else:
                    arrowWidth = 3
                    arrowColor = "royalblue"
            passArrow = plt.Arrow(x, y, dx, dy, width = arrowWidth, color = arrowColor)
            ax.add_patch(passArrow)
        
        if (len(oppositeTeam) == 0 and p['team_id'] != teamID):
                oppositeTeam = p['team_name']

    title = "output/" + playerName + "_passes_" + oppositeTeam + ".png"
    # ax.set_title(title, fontsize = 24)
    plt.show()
    fig.set_size_inches(10, 7)
    fig.savefig(title, dpi = 800, transparent=True)
    
def drawPlayerGoals(matchShots, teamID, playerName):
    ''' 
    Parameters :
        matchShots : DataFrame
        teamID     : int
        playerName : string

    Returns    :
        A pitch with arrows representing 
        the goals (dark blue) and the shots (light blue) 
        from a given player, during a given match.
    '''

    # Draw the pitch
    pitch   = Pitch(line_color = "black", linewidth = 3)
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plot the passes on the pitch
    oppositeTeam = ""
    for i, s in matchShots.iterrows():
        if s['player_name'] == playerName:
            # Plot circles
            x          = s['x']
            y          = s['y']
            goal       = s['outcome_name'] == 'Goal'
            if goal :
                shotCircle = plt.Circle((x, y), 3, color = "blue")
            else:
                shotCircle = plt.Circle((x, y), 3, color = "royalblue")
                shotCircle.set_alpha(.7)
            ax.add_patch(shotCircle)

        if (len(oppositeTeam) == 0 and s['team_id'] != teamID):
                oppositeTeam = s['team_name']

    title = "output/" + playerName + "_goals_" + oppositeTeam + ".png"
    # ax.set_title(title, fontsize = 24)
    plt.show()
    fig.set_size_inches(10, 7)
    fig.savefig(title, dpi = 800, transparent=True)

##### OPENING COMPETITION DATA SET #####

parser          = Sbopen()
dfCompetition   = parser.competition()


##### OPENING EURO 2020 DATA SET #####

competitionID   = 55
seasonID        = 43
dfMatch         = parser.match(competitionID, seasonID)


#####
franceID           = 771
franceGameList     = getGameIDList(dfMatch, 'France')

##### AVERAGE xG #####

# averageXgEuro      = getCompetitionAverageXg(dfMatch)
# nShotsEuro         = getCompetitionShotsNumber(dfMatch)
# nGoalsEuro         = getCompetitionGoalsNumber(dfMatch)

# nShotsBenzema      = getPlayerShotsNumber(dfMatch, franceGameList, 'Karim Benzema')
# nGoalsBenzema      = getPlayerGoalsNumber(dfMatch, franceGameList, 'Karim Benzema')
# averageXgBenzema   = getPlayerAverageXg(dfMatch, franceGameList, 'Karim Benzema')

# nShotsMbappe       = getPlayerShotsNumber(dfMatch, franceGameList, 'Kylian Mbappé Lottin')
# nGoalsMbappe       = getPlayerGoalsNumber(dfMatch, franceGameList, 'Kylian Mbappé Lottin')
# averageXgMbappe    = getPlayerAverageXg(dfMatch, franceGameList, 'Kylian Mbappé Lottin')

# nShotsGriezmann    = getPlayerShotsNumber(dfMatch, franceGameList, 'Antoine Griezmann')
# nGoalsGriezmann    = getPlayerGoalsNumber(dfMatch, franceGameList, 'Antoine Griezmann')
# averageXgGriezmann = getPlayerAverageXg(dfMatch, franceGameList, 'Antoine Griezmann')


##### PASSES #####

for matchID in franceGameList:
    matchPasses      = getMatchPasses(dfMatch, matchID)
    keyPassIndexList = getKeyPassIndexList(dfMatch, matchID)
    matchShots       = getMatchShots(dfMatch, matchID)
    drawPlayerPasses(matchPasses, keyPassIndexList, franceID, 'Karim Benzema')
    drawPlayerGoals(matchShots, franceID, 'Karim Benzema')
    drawPlayerPasses(matchPasses, keyPassIndexList, franceID, 'Kylian Mbappé Lottin')
    drawPlayerGoals(matchShots, franceID, 'Kylian Mbappé Lottin')
    drawPlayerPasses(matchPasses, keyPassIndexList, franceID, 'Antoine Griezmann')
    drawPlayerGoals(matchShots, franceID, 'Antoine Griezmann')




    

        