import pandas as pd
from random import randint

class Player:
    def __init__(self, player_id):

        # load player info
        self.players = pd.read_csv('Showdown_Charts.csv')
        player_df = self.players.loc[self.players['ID'] == player_id].iloc[0]

        # get list of pitchers and batters to randomly draw from
        pitcher_positions = ['Starter', 'Reliever', 'Closer']
        self.pitchers = self.players[self.players.Position1.isin(pitcher_positions)]
        self.batters = self.players[~self.players.Position1.isin(pitcher_positions)]

        # get On-base
        self.on_base = int(player_df.OnBase)

        # create dict for fast chart lookup
        self.chart = dict()

        for i in range(1,31):
            self.chart[i] = self.lookup_result(i, player_df)
        
    def lookup_result(self,  swing, player):
        result_cols = ['PU', 'SO', 'GB', 'FB', 'BB', 'Single', 'SinglePlus', 'Double', 'Triple', 'HR']

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
        
        # if number isn't found it's probably a 2000/2001 card and swing>20
        # return whatever the result is for 20
        return self.lookup_result(20, player)
    
    # def get_random_pitcher():
    #     pitcher_id = randint(1,max(self.pitchers.ID))
    #     pitcher = 
    #     self.pitchers = p
        

    def simulate_random_ab():



        pass