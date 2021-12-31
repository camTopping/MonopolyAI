import pandas as pd
from plotnine import ggplot, aes, geom_line, facet_wrap

def plot_metrics(df ,number_of_players):
    column_names = [f'Player{i}' for i in range(1, number_of_players + 1)]
    df = pd.DataFrame(df, columns=column_names)
    df["turn"] = df.index
    # Pivot wide to long table format
    df = pd.melt(df, id_vars=["turn"], value_vars=column_names)
    df = df.rename(columns={"variable": "player", "value": "money"})

    g = (ggplot(df, aes('turn', 'money', color='factor(player)')) +
         geom_line())

    return g
