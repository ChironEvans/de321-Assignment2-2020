def date_works(date):
    result = False
    if date == '2018-02-17':
        result = True
    return result


def type_works(match_type):
    result = False
    if match_type == 'Match Type':
        result = True
    return result


def team1_works(team1):
    result = False
    if team1 == 'Team 1':
        result = True
    return result


def team2_works(team2):
    result = False
    if team2 == 'Team 2':
        result = True
    return result


def winner_works(winner):
    result = False
    if winner == 'Winner':
        result = True
    return result


def mvp_works(mvp):
    result = False
    if mvp == 'MVP':
        result = True
    return result


def toss_winner_works(toss_winner):
    result = False
    if toss_winner == 'toss_winner':
        result = True
    return result

def toss_decision_works(toss_decision):
    result = False
    if toss_decision == 'toss_decision':
        result = True
    return result

def umpire_works(umpire, list_length):
    result = False
    umpire_name_works = False
    umpire_list_works = False
    if umpire == 'Umpire 1':
        umpire_name_works = True
    if list_length == 2:
        umpire_list_works = True
    if umpire_name_works == True and umpire_list_works == True:
        result = True

    return result

def venue_works(venue):
    result = False
    if venue == 'Venue':
        result = True
    return result

def string_works(returned):
    result = False
    expected = ['Cricket Match Info: ', 'Date: 2018-02-17 ',
                ' Match Type: Match Type ', 'Teams:  ', 'Match Winner: Winner ',
                'MVP: MVP ', 'Toss Winner: toss_winner ',
                'Toss Decision: toss_decision ', 'Venue: Venue ', 'Umpires: ',
                '   Umpire 1', '   Umpire 2']
    if returned == expected:
        result = True

    return result
