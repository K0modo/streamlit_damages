import pandas as pd
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
data_file = current_dir / "data" / "main_city_surcharges_may1.csv"
df = pd.read_csv(data_file)

month_num = ["01","02","03","04","05","06","07","08","09","10","11","12"]
seasons = ["Winter", "Winter", "Spring", "Spring", "Spring", "Summer", "Summer",
           "Summer", "Fall", "Fall", "Fall", "Winter"]
zipped_seasons = dict(zip(month_num, seasons))
zipped_seasons
season_df = df.groupby('Period', as_index=False)['Damages'].sum()
season_df['Month'] = season_df['Period'].astype(str)
season_df['Month'] = season_df['Month'].str[-2:]
season_df['Month'] = season_df['Month'].replace(zipped_seasons)



