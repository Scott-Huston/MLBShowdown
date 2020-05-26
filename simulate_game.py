from random import randint
import pandas as pd

### example lineups
# home_lineup = [[2912, 'LF-RF'],
#                 [455, 'C'],
#                 [695, 'LF-RF'],
#                 [3677, 'DH'],
#                 [289, '2B'],
#                 [2657, '3B'],
#                 [201, '1B'],
#                 [1104, 'SS'],
#                 [3807, 'CF']]

class Game:
    def __init__(self, home_lineup, home_pitching_dict, away_lineup, away_pitching_dict):
        # TODO add strategy settings for stealing/bunting and maybe icons/random bonuses
        # TODO implement batter classes to keep track of stats and icon/bonus usage
        self.home_lineup = home_lineup
        self.home_pitching_dict = home_pitching_dict
        self.away_lineup = away_lineup
        self.away_pitching_dict = away_pitching_dict

        self.inning = 1
        self.outs = 0
        self.runners = {1:None, 2:None, 3:None, 4:[]}
        self.home_score = 0
        self.away_score = 0
        self.home_batter = 1
        self.away_batter = 1
        self.players = pd.read_csv('Showdown_Charts.csv')
        self.home_defense = self.get_def_scores(self.home_lineup)
        self.away_defense = self.get_def_scores(self.away_lineup)

    def get_def_scores(self, lineup):
        IF_positions = ['1B', '2B', 'SS', '3B']
        OF_positions = ['LF-RF', 'CF']

        defense = {'C':0,
                    'IF':0,
                    'OF':0}

        for entry in lineup:
            player = self.players.loc[self.players['ID'] == entry[0]].iloc[0]

            ### Getting catcher score ###
            if entry[1] == 'C':
                # check Position1 (checking for 'C+' so CF isn't counted)
                if 'C+' in player.Position1:
                    fielding_score = int(player.Position1.split('+')[-1])
                    defense['C'] = fielding_score
                # check Position2
                elif 'C+' in player.Position2:
                    fielding_score = int(player.Position2.split('+')[-1])
                    defense['C'] = fielding_score
                else:
                    raise ValueError(f'player {entry[0]} in invalid position')
            
            ### Getting IF score ###
            if entry[1] in IF_positions:
                # check Position1 
                if entry[1] in player.Position1 or 'IF' in player.Position1:
                    fielding_score = int(player.Position1.split('+')[-1])
                    defense['IF'] += fielding_score
                # check Position2
                elif entry[1] in player.Position2 or 'IF' in player.Position1:
                    fielding_score = int(player.Position2.split('+')[-1])
                    defense['IF'] += fielding_score
                else:
                    raise ValueError(f'player {entry[0]} in invalid position')
            
            ### Getting OF score ###
            if entry[1] in OF_positions:
                # check Position1 
                if entry[1] in player.Position1 or 'OF' in player.Position1:
                    fielding_score = int(player.Position1.split('+')[-1])
                    defense['OF'] += fielding_score
                # check Position2
                elif entry[1] in player.Position2 or 'OF' in player.Position1:
                    fielding_score = int(player.Position2.split('+')[-1])
                    defense['OF'] += fielding_score
                else:
                    raise ValueError(f'player {entry[0]} in invalid position')
            
        return defense
    
    def lookup_result(self,  swing, advantage_player_id):
        result_cols = ['PU', 'SO', 'GB', 'FB', 'BB', 'Single', 'SinglePlus', 'Double', 'Triple', 'HR']
        player = self.players.loc[self.players['ID'] == advantage_player_id]

        # iterate through results to find one containing swing
        for col in result_cols:
            res_range = player[col][0].strip('\'').split('-')
            if res_range[0] != '':
                # convert to ints
                res_range = [int(r) for r in res_range]
                if res_range[0] <= swing and res_range[-1] >= swing:
                    return col
    
    def apply_result(self, result, home_team_up, batter):
        """
        Move runners, add scores, add outs, change batter
        """

        result_cols = ['PU', 'SO', 'GB', 'FB', 'BB', 'Single', 'SinglePlus', 'Double', 'Triple', 'HR']

        if result in ['PU', 'SO']:
            self.outs += 1
        if result == 'GB':
            # double-play logic
            if self.outs < 2:
                if self.runners[1]:
                    speed = batter.Speed[0]

        

        if home_team_up:
            self.home_batter += 1
        else:
            self.away_batter += 1
            
        #TODO finish this
        pass

    def at_bat(self, pitcher_id, hitter_id):
        pitch = randint(1,20)
        swing = randint(1,20)

        pitcher = self.players.loc[self.players['ID'] == pitcher_id]
        batter = self.players.loc[self.players['ID'] == batter_id]

        control = pitcher.Control[0]
        on_base = batter.OnBase[0]
        # TODO change so pitchers can hit (their on_base is 'NA')

        if (control + pitch) > on_base:
            advantage_player_id = pitcher_id
        else:
            advantage_player_id = hitter_id

        # TODO finish this
        pass

        





    
    def simulate_home_batting(self):
        
        pass


    def simulate_game(home_lineup, home_pitching_dict, away_lineup, away_pitching_dict):
        pass
