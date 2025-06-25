import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Make "raw" data - all data plus date column and renamed columns and reordered
# I don't touch the actual data
# Replace 'path/to/ALTU_ALL.csv' with the actual path to your file
file_path = 'ALTU_ALL.csv'

try:
    df_altu = pd.read_csv(file_path)
    print("ALTU_ALL file loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# prompt: make a datetime column in the altu dataframe from the day month and year columns. the month columns is the abbreviated text (e.g., "JAN")
df_altu['Date'] = pd.to_datetime(df_altu['month'] + ' ' + df_altu['day'].astype(str) + ', ' + df_altu['year'].astype(str), format='%b %d, %Y')

df_altu = df_altu.set_index('Date')


new_cols = {"pool": "pool_0800",
            "elevations (ft)": "pool_2400",
            "storage (2400hr)": "storage",
            "releases (power)": "releases_power",
            "releases (total)": "releases_total",
            "evap inches": "evaporation",
            "inflow adj": "inflow",
            "rainfall inches (7A to Dam)": "rain_dam",
            "rainfall inches (7A to BSN)": "rain_bsn"}

df_altu = df_altu.rename(columns = new_cols)

df_altu = df_altu[['day', 'month', 'year', 'pool_0800', 'pool_2400', 'storage',
                   'releases_power', 'releases_total', 'evaporation', 'inflow',
                   'rain_dam', 'rain_bsn']]

df_altu = df_altu.sort_index()

df_altu.to_csv("lugert_altus_data_1994_2024.csv")
df_altu_raw = df_altu.copy()

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# Make "clean" 
df_altu['pool_0800'] = df_altu['pool_0800'].where(df_altu['pool_0800'] > 1400)
df_altu['pool_2400'] = df_altu['pool_2400'].where(df_altu['pool_2400'] > 1400)
df_altu['storage'] = df_altu['storage'].where(df_altu['storage'] > 10)
df_altu['storage'] = df_altu['storage'].where(df_altu['storage'] < 160000)

df_altu.to_csv("lugert_altus_data_1994_2024_CLN.csv")


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Make "1995" data
df_95 = df_altu.loc['1995']
df_95.to_csv("lugert_altus_data_1995_CLN.csv")

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Make "Aug 1995" data
df_altu.loc['1995-08'].to_csv("lugert_altus_data_Aug_1995_CLN.csv")


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Make storage plot 


ax = df_altu["storage"].plot(figsize=(10, 5))
ax.grid()
ax.set_ylabel('Storage (ac-ft)')
ax.set_xlabel('Date')
ax.set_title('Water storage in Lake Lugert-Altus')
plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/storage_time_series.png')
plt.clf()


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Make average annual rainfall data

annual_rainfall = df_altu.groupby(df_altu.index.year)['rain_bsn'].sum()

ax = annual_rainfall.plot.bar(figsize=(10, 4))
ax.grid(axis='y')
ax.set_ylabel('Rainfall (in)')
ax.set_xlabel('Year')
ax.set_title('Annual rainfall in Lake Lugert-Altus watershed')
plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/annual_average_rainfall.png')
plt.clf()


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Make storage plot for 1995

df_95 = df_altu.loc['1995']

ax = df_95['storage'].plot(grid=True, figsize=(10, 5))
ax.set_ylabel('Storage (ac-ft)')
ax.set_xlabel('Date')
ax.set_title('Reservoir storage at Lake Lugert-Altus in 1995')
plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/1995_storage.png')
plt.clf()

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Make storage and rainfall plot for 1995


fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_95.index, df_95['storage'], label='Storage', color='blue')
ax.grid()

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

ax2 = ax.twinx()

# Add bar plot to same axes
ax2.bar(df_95.index, df_95['rain_bsn'], label='Rainfall', color='green', alpha=0.7, width=1)

ax.set_yticks(np.linspace(20000, 160000, 8))
ax2.set_yticks(np.linspace(0, 3.5, 8))


ax.set_ylabel('Reservoir Storage')
ax2.set_ylabel('Rainfall (inches)')

# get handles for ax and ax2
line_handles, line_labels = ax.get_legend_handles_labels()
bar_handles, bar_labels = ax2.get_legend_handles_labels()

# Combine them
all_handles = line_handles + bar_handles 
all_labels = line_labels + bar_labels 

# Add legend to ax1 (or ax2 if you prefer)
ax.legend(all_handles, all_labels, loc='upper left')

ax.set_title('Reservoir Storage and Rainfall at Lake Lugert-Altus, 1995')
plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/storage_rain_1995.png')

# add in the releases
release_color = 'orange'
ax3 = ax.twinx()
ax3.spines["right"].set_position(("axes", 1.1))  # Offset this axis
ax3.bar(df_95.index, df_95['releases_total'], color=release_color, alpha=0.5, width=1, label='Releases (Top Down)')
ax3.set_ylabel('Releases (daily avg CFS)', color=release_color)
ax3.tick_params(axis='y', labelcolor=release_color)


ax3.set_yticks(np.linspace(0, 7000, 8))
ax3.set_ylim(0, 7000)

ax3.invert_yaxis()

# Get handles and labels from both axes
release_handles, release_labels = ax3.get_legend_handles_labels()

# Combine them
all_handles = line_handles + bar_handles + release_handles
all_labels = line_labels + bar_labels + release_labels

# Add legend to ax1 (or ax2 if you prefer)
ax.legend(all_handles, all_labels, loc='upper left')

ax.set_title('')
ax.set_title('Reservoir Storage, Rainfall, and Releases \n at Lake Lugert-Altus, 1995', backgroundcolor='white')
plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/storage_rain_releases_1995.png')
plt.clf()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Make Streamflow plot

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_95.index, df_95['inflow'], label='Inflow', color='orange', alpha=0.7)
ax.grid()

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

ax2 = ax.twinx()

# Add bar plot to same axes
ax2.bar(df_95.index, df_95['rain_bsn'], label='Rainfall', color='green', alpha=0.5, width=1)

ax.set_yticks(np.linspace(0, 16000, 8))
# ax2.set_yticks(np.linspace(0, 3.5, 8))
ax.set_ylim(0, 16000)
# ax2.set_ylim(0, 3.5)

ax.set_ylabel('Reservoir Inflow (CFS)')
ax2.set_ylabel('Basin Rainfall (inches)')

# Get handles and labels from both axes
line_handles, line_labels = ax.get_legend_handles_labels()
bar_handles, bar_labels = ax2.get_legend_handles_labels()

# Combine them
all_handles = line_handles + bar_handles
all_labels = line_labels + bar_labels

# Add legend to ax1 (or ax2 if you prefer)
ax.legend(all_handles, all_labels, loc='upper left')

plt.title('Reservoir Inflow and Rainfall at Lake Lugert-Altus, 1995')
plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/rainfall_inflow.png')
plt.clf()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Storage - pool plot - raw
ax = df_altu_raw.plot(kind='scatter', x='pool_0800', y='storage', s=4, alpha=.8)
ax.grid()
ax.set_ylabel('Storage (ac-ft)')
ax.set_xlabel('Pool Elevation at 0800 (ft NGVD)')
ax.set_title('Storage - Elevation Relation at Lake Lugert-Altus')

plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/storage_elevation_raw.png')
plt.clf()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Storage - pool plot - clean
ax = df_altu.plot(kind='scatter', x='pool_0800', y='storage', s=4, alpha=.8)
ax.grid()
ax.set_ylabel('Storage (ac-ft)')
ax.set_xlabel('Pool Elevation at 0800 (ft NGVD)')
ax.set_title('Storage - Elevation Relation at Lake Lugert-Altus')

plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/storage_elevation.png')
plt.clf()


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Storage - pool plot - colored
ax = df_altu.plot(kind='scatter', c='year', x='pool_0800', y='storage', s=4, alpha=.8, cmap='viridis')
ax.grid()
ax.set_ylabel('Storage (ac-ft)')
ax.set_xlabel('Pool Elevation at 0800 (ft NGVD)')
ax.set_title('Storage - Elevation Relation at Lake Lugert-Altus')

plt.tight_layout()
plt.savefig('../../images/blog/250624_k12_wkshp/storage_elevation_color.png')
plt.clf()





