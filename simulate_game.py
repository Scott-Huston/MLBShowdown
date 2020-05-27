from random import randint
import pandas as pd

### example lineup
home_lineup = [[2912, 'LF-RF'],
                [455, 'C'],
                [695, 'LF-RF'],
                [3677, 'DH'],
                [289, '2B'],
                [2657, '3B'],
                [201, '1B'],
                [1104, 'SS'],
                [3807, 'CF']]

### example pitching_dict
home_pitching_order = [152,152,152,152,152,152,152,1524,1524,1524]

class Game:
    def __init__(self, home_lineup, home_pitching_order, away_lineup, away_pitching_order):
        # TODO add strategy settings for stealing/bunting and maybe icons/random bonuses
        # TODO implement batter classes to keep track of stats and icon/bonus usage
        self.home_lineup = home_lineup
        self.home_pitching_order = home_pitching_order
        self.away_lineup = away_lineup
        self.away_pitching_order = away_pitching_order

        self.inning = 1
        self.outs = 0
        self.runners = {1:None, 2:None, 3:None, 4:[]}
        self.home_score = 0
        self.away_score = 0
        self.home_batter = 0
        self.away_batter = 0
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
        player = self.players.loc[self.players['ID'] == advantage_player_id].iloc[0]

        # iterate through results to find one containing swing
        for col in result_cols:
            res_range = player[col].strip('\'').split('-')
            if res_range[0] != '':
                # check for +
                if '+' in res_range[0]:
                    res_range[0] = res_range[0].split('+')[0]
                    res_range.append(100)
                # convert to ints
                res_range = [int(r) for r in res_range]
                if res_range[0] <= swing and res_range[-1] >= swing:
                    return col
    
    def apply_result(self, result, home_team_up, batter, verbose=0):
        """
        Move runners, add scores, add outs, change batter
        """

        #TODO add ability to take extra bases on Single, SinglePlus, Double, and FB

        if result in ['PU', 'SO']:
            self.outs += 1
        if result == 'GB':
            self.outs += 1
            batter_to_first = False
            # double-play logic
            if self.outs < 3 and self.runners[1]:
                # remove lead runner
                self.runners[1] = None

                roll = randint(1,20)

                if verbose>1:
                    print(f'Roll for double-play = {roll}')

                if home_team_up:
                    fielding = self.home_defense['IF']
                else:
                    fielding = self.away_defense['IF']

                fielding_check = roll + fielding

                if fielding_check > batter.Speed:
                    self.outs += 1
                else:
                    batter_to_first=True

            # runners advance
            self.advance_runners()
            if batter_to_first:
                self.runners[1] = batter.ID

        if result == 'FB':
            #TODO add tagging up logic
            self.outs += 1
        
        if result == 'BB':
            self.advance_runners()
            self.runners[1] = batter.ID
        
        if result == 'Single':
            self.advance_runners()
            self.runners[1] = batter.ID
        
        if result == 'SinglePlus':
            self.advance_runners()
            
            if self.runners[2] == None:
                self.runners[2] = batter.ID
            else:
                self.runners[1] = batter.ID
        
        if result == 'Double':
            self.advance_runners(num_bases=2)
            self.runners[2] = batter.ID
        
        if result == 'Triple':
            self.advance_runners(num_bases=3)
            self.runners[3] = batter.ID
        
        if result == 'HR':
            self.advance_runners(num_bases=3)
            self.runners[4].append(batter.ID)

        # bookkeeping
        if home_team_up:
            self.home_batter = (self.home_batter+1)%9
            self.home_score += len(self.runners[4])
        else:
            self.away_batter = (self.home_batter+1)%9
            self.away_score += len(self.runners[4])
        
        self.runners[4] = []

    def advance_runners(self, num_bases=1):
        if self.outs < 3:
            for _ in range(num_bases):
                if self.runners[3]:
                    self.runners[4].append(self.runners[3])
                    self.runners[3] = None
                if self.runners[2]:
                    self.runners[3] = self.runners[2]
                    self.runners[2] = None
                if self.runners[1]:
                    self.runners[2] = self.runners[1]
                    self.runners[1] = None

    def at_bat(self, pitcher_id, batter_id, home_team_up, verbose=0):
        # TODO add pitcher tiring
        pitch = randint(1,20)
        swing = randint(1,20)

        if verbose>1:
            print(f'Pitch: {pitch}')
            print(f'Swing: {swing}')

        pitcher = self.players.loc[self.players['ID'] == pitcher_id].iloc[0]
        batter = self.players.loc[self.players['ID'] == batter_id].iloc[0]

        control = pitcher.Control
        on_base = batter.OnBase
        # TODO change so pitchers can hit (their on_base is 'NA')

        if (control + pitch) > on_base:
            advantage_player_id = pitcher_id
        else:
            advantage_player_id = batter_id

        result = self.lookup_result(swing, advantage_player_id)
        self.apply_result(result, home_team_up, batter, verbose)

        if verbose>0:
            print(result)
            if self.runners[3]:
                print(f'{self.runners[3]} on third')
            if self.runners[2]:
                print(f'{self.runners[2]} on second')
            if self.runners[1]:
                print(f'{self.runners[1]} on first')

    def simulate_away_batting(self, verbose=0):
        pitcher_id = self.home_pitching_order[self.inning]
        while self.outs<3:
            batter_id = self.away_lineup[self.away_batter][0]
            self.at_bat(pitcher_id, batter_id, True,verbose)

        self.reset_inning()

        if verbose:
            print(f'End top of inning number {self.inning}')
    
    def simulate_home_batting(self, verbose=0), walkoff_potential=False:
        pitcher_id = self.away_pitching_order[self.inning]
        while self.outs<3:
            batter_id = self.home_lineup[self.home_batter][0]
            self.at_bat(pitcher_id, batter_id, True,verbose)

            if walkoff_potential and self.home_score>self.away_score:
                break

        self.reset_inning()

        if verbose:
            print(f'End bottom of inning number {self.inning}')
    
    def reset_inning(self):
        self.outs = 0
        self.runners = {1:None, 2:None, 3:None, 4:[]}

    def simulate_game(self, verbose=0):
        for _ in range(8):
            self.simulate_away_batting(verbose=verbose)
            self.simulate_home_batting(verbose=verbose)
            self.inning += 1

        
        self.simulate_away_batting(verbose=verbose)
        
        if not self.home_score > self.away_score:
            self.simulate_home_batting(verbose=verbose, walkoff_potential=True)

        # TODO account for extra innings pitcher selection
        while self.home_score == self.away_score:
            self.simulate_away_batting(verbose=verbose)

            if not self.home_score > self.away_score:
                self.simulate_home_batting(verbose=verbose, walkoff_potential=True)
        
        if self.home_score>self.away_score:
            winner = 'Home team'
        else:
            winner = 'Away team'

        print(f'{winner} wins {self.home_score} to {self.away_score}')
