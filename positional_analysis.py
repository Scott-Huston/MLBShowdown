import pandas as pd
from scipy import stats
import seaborn as sns

players = pd.read_csv('Showdown_Charts_Expanded.csv')

# formula for est_wOBA from here http://www.3-dbaseball.net/2009/11/converting-obpslg-to-woba.html
"""
x = .56*OBP + .31*SLG
wOBA = -.53x^2 + 1.35x - .045
"""

batters = players[players['Role']=='Batter']
pitcher_roles = ['Starter', 'Reliever']
pitchers = players[players['Role'].isin(pitcher_roles)]

batters['x'] = (.56*batters['OBP_350'])+.31*batters['SLG_350']
batters['est_wOBA'] = (-.53*(batters['x']**2)) + (1.35*batters['x'])-.045

pitchers['x'] = (.56*pitchers['oOBP_350'])+.31*pitchers['oSLG_350']
pitchers['est_wOBA'] = (-.53*(pitchers['x']**2)) + (1.35*pitchers['x'])-.045

batters['Z_est_wOBA'] = stats.zscore(batters['est_wOBA'])
pitchers['Z_est_wOBA'] = stats.zscore(pitchers['est_wOBA'])

#####################

positions = ['C', '1B', '2B', 'SS', '3B', 'LFRF', 'CF']

pos_dfs = dict()



for pos in positions:
    col = f'Def_{pos}'
    pos_dfs[pos] = batters[batters[col].notnull()]
    pos_dfs[pos][f'{pos}_Z_est_wOBA'] = stats.zscore(pos_dfs[pos]['est_wOBA'])


pos_dfs_list = [x for x in pos_dfs.values()]

players2 = pd.DataFrame()
for df in pos_dfs_list:
    players2 = players2.append(df)

position_Z_est_columns = [f'{pos}_Z_est_wOBA' for pos in positions]

players2["pos_Z_est_wOBA"] = players2[position_Z_est_columns].max(axis=1)



players2.s








