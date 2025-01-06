import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib import colormaps
from matplotlib.lines import Line2D
from matplotlib.colors import BoundaryNorm

# Load filtered dataset
df = pd.read_json('data/filtered_data.json')

### --- MOST COMMON MOTIFS, MOTIF GROUPS AND CHRISTIAN MOTIFS --- ###

# Split motifs into individual entries for analysis
df['motif_list'] = df['motifs'].str.split(', ')

# Flatten the motif list for easier counting
all_motifs = pd.Series([m for sublist in df['motif_list'] for m in sublist])

# Get counts of all motifs
motif_counts = all_motifs.value_counts()

# Do the same for motif-groups
df['motif_group_list'] = df['motif_group'].str.split(', ')
all_motif_groups = pd.Series([group for sublist in df['motif_group_list'] for group in sublist if group]) 
motif_group_counts = all_motif_groups.value_counts()
top_motif_groups = motif_group_counts.nlargest(10)

# Create barplot 
def create_barplot(data, title, xlabel, ylabel, figsize=(10, 6,), palette='viridis'):
    plt.figure(figsize=figsize)
    sns.barplot(y=data.index, x=data.values, palette=palette)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

create_barplot(motif_counts.head(25), 'Top 25 Most Common Motifs', 'Frequency', 'Motifs', figsize=(10, 12))
create_barplot(top_motif_groups, 'Top 10 Most Common Motif Groups', 'Frequency', 'Motif Groups', figsize=(12, 12))
print(top_motif_groups)

# Create barplot for the most common motifs that are identified as christian 
# Get count
top_motifs = motif_counts.head(15).index  
top_motif_counts_by_christian = df.explode('motif_list')
top_motif_counts_by_christian = top_motif_counts_by_christian[top_motif_counts_by_christian['motif_list'].isin(top_motifs)]
top_motif_counts = top_motif_counts_by_christian.groupby(['motif_list', 'christian']).size().unstack(fill_value=0)

# Reorder columns 
top_motif_counts = top_motif_counts[['yes', 'no']] 

# Filter and sort motifs with a "christian: yes" status
top_motif_counts_yes = top_motif_counts[top_motif_counts['yes'] > 0]  
top_motif_counts_yes = top_motif_counts_yes.sort_values('yes', ascending=True)

# Create bar plot 
colors = ['#bcbd22', '#9467bd'] 
top_motif_counts_yes.plot(kind='barh', stacked=True, figsize=(10, 12), color=colors)

plt.title('Most common Motifs on proven Christian Epitaphs')
plt.xlabel('Frequency')  
plt.ylabel('Motifs')     
plt.legend(title='christian')
plt.tight_layout()
plt.show()


### --- CHRONOLOGICAL TRENDS --- ###

# Convert 'not_before' and 'not_after' to integers
df['not_before'] = pd.to_numeric(df['not_before'], errors='coerce')
df['not_after'] = pd.to_numeric(df['not_after'], errors='coerce')

# Average date (approximation for trends)
df['average_date'] = (df['not_before'] + df['not_after']) / 2

# Group motifs by time range
chronological_data = (
    df.explode('motif_list')
    .groupby(['average_date', 'motif_list'])
    .size()
    .unstack(fill_value=0)
)

# Create 50-year bins 
bins = list(range(200, 700, 50))  # Example range: 500 BCE to 500 CE
labels = [f"{start} to {start + 49}" for start in bins[:-1]]

# Add a 'date_bin' column to the DataFrame
df['date_bin'] = pd.cut(
    df['average_date'], 
    bins=bins, 
    labels=labels, 
    right=False  
)

# Group motifs by date_bin
binned_data = (
    df.explode('motif_list')
    .groupby(['date_bin', 'motif_list'])
    .size()
    .unstack(fill_value=0)
)

# Group motif groups by time range
binned_group_data = (
    df.explode('motif_group_list')
    .groupby(['date_bin', 'motif_group_list'])
    .size()
    .unstack(fill_value=0)
)
# print(binned_group_data)
# print(motif_group_counts) 
print(top_motif_groups) 

# calculate frequency of each motif and select the top 25 and top 10
top_25_motifs = binned_data.sum(axis=0).nlargest(25).index
top_10_motifs = binned_data.sum(axis=0).nlargest(10).index
binned_data_top_25 = binned_data[top_25_motifs]
binned_data_top_10 = binned_data[top_10_motifs]
# ubset binned_group_data for the global top 10 motif groups
binned_group_data_top_10 = binned_group_data[top_motif_groups.index]

# create Line Plot
def create_lineplot(data, title, xlabel, ylabel, figsize=(14, 8), linewidth=2, legend_title='Legend'):
    
    data.plot(kind='line', figsize=figsize, linewidth=linewidth)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend placement
    plt.tight_layout()
    plt.show()

create_lineplot(
    data=binned_data_top_10,
    title='Chronological Trends of Top 10 Motifs (Line Plot)',
    xlabel='50-Year Time Bin',
    ylabel='Frequency',
    figsize=(14, 8),
    linewidth=2,
    legend_title='Motifs'
)

# create Line Plot for Motif Groups 

create_lineplot(
    data=binned_group_data_top_10,
    title='Chronological Trends of Top 10 Motif Groups (Line Plot)',
    xlabel='50-Year Time Bin',
    ylabel='Frequency',
    figsize=(14, 8),
    linewidth=2,
    legend_title='Motif Groups'
)

# Create Heatmap 

def create_heatmap(data, title, xlabel, ylabel, cmap='coolwarm', figsize=(12, 8), colorbar_label='Frequency'):
    plt.figure(figsize=figsize)
    sns.heatmap(data, cmap=cmap, cbar_kws={'label': colorbar_label})
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

create_heatmap(binned_data_top_25.T, 'Chronological Trends of Top 25 Motifs (Heatmap)', 
               'Average Date', 'Motifs', cmap='coolwarm', figsize=(14, 8))

create_heatmap(binned_group_data_top_10.T, 'Chronological Trends of Top 10 Motif Groups (Heatmap)', 
               'Average Date', 'Motif Groups', cmap='coolwarm', figsize=(14, 8))


### --- GEOGRAPHICAL TRENDS --- ###

# load world geometries 
world = gpd.read_file('mapdata/ne_110m_admin_0_countries.shp')
country_counts = df['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

# merge world DataFrame with the country counts
world = world.merge(country_counts, how="left", left_on="ADMIN", right_on="country")

# map motifs to colors
def map_colors(unique_motifs, default_color='white', color_map='tab10'):
    colors = colormaps[color_map] 
    motif_color_map = {motif: colors(i) for i, motif in enumerate(unique_motifs)}
    return motif_color_map

# plot world map with motifs
def plot_motif_map(world, unique_motifs, motif_color_map, title, default_color='white'):
    world['color'] = world['common_motif'].map(motif_color_map).fillna(default_color)
    
    # figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    world.boundary.plot(ax=ax, linewidth=1, color='k')  # boundaries
    world.plot(color=world['color'], ax=ax, legend=False)  # fill countries
    
    plt.title(title)
    
    # legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=str(motif),
                               markerfacecolor=motif_color_map[motif], markersize=10)
                       for motif in unique_motifs]
    legend_elements.append(Line2D([0], [0], marker='o', color='w', label='Not in Dataset',
                                   markerfacecolor=default_color, markersize=10))
    ax.legend(handles=legend_elements, title="Most Common Motif", loc='upper right')
    plt.show()

# flatten the motif list for easier counting
motif_with_country = df.explode('motif_list')[['country', 'motif_list', 'average_date']]

# show top motifs for each country (total, before and after 350 a.c.)
def process_motifs(world, motif_with_country, title, year_filter=None):
   
    motif_with_country['average_date'] = pd.to_numeric(motif_with_country['average_date'], errors='coerce')

    if year_filter == 'before':
        motif_data = motif_with_country[motif_with_country['average_date'] < 350]
    elif year_filter == 'after':
        motif_data = motif_with_country[motif_with_country['average_date'] >= 350]
    else:
        motif_data = motif_with_country  # No filter applied

    if motif_data.empty:
        print(f"No data found for motifs {year_filter}.")
        return

    # croup motifs by country and count occurrences
    motif_counts = motif_data.groupby(['country', 'motif_list']).size().reset_index(name='counts')
    most_common_motif = motif_counts.loc[motif_counts.groupby('country')['counts'].idxmax()]
    most_common_motif = most_common_motif.rename(columns={'motif_list': 'common_motif'})

    # merge the motifs into the world GeoDataFrame
    world_with_motif = world.merge(most_common_motif, how="left", left_on="ADMIN", right_on="country")

    # handle potential column name conflicts
    if 'common_motif_y' in world_with_motif.columns:
        world_with_motif = world_with_motif.rename(columns={'common_motif_y': 'common_motif'})

    # map colors
    unique_motifs = world_with_motif['common_motif'].dropna().unique()
    motif_color_map = map_colors(unique_motifs)

    # plot results
    plot_motif_map(world_with_motif, unique_motifs, motif_color_map, title)


process_motifs(world, motif_with_country, "Most Common Motif by Country")
process_motifs(world, motif_with_country, "Most Common Motif by Country (Before Year 350)", year_filter='before')
process_motifs(world, motif_with_country, "Most Common Motif by Country (After Year 350)", year_filter='after')


# calculate total finds before and after the year 350
def calculate_finds(motif_with_country, year_threshold=350):
    # count finds before 
    finds_before = motif_with_country[motif_with_country['average_date'] < year_threshold]
    total_finds_before = finds_before.groupby('country').size().reset_index(name='total_finds_before')

    # count finds after 
    finds_after = motif_with_country[motif_with_country['average_date'] >= year_threshold]
    total_finds_after = finds_after.groupby('country').size().reset_index(name='total_finds_after')

    # count total finds for all years
    total_finds_all_years = motif_with_country.groupby('country').size().reset_index(name='total_finds_all_years')
    
    return total_finds_before, total_finds_after, total_finds_all_years

total_finds_all_years, total_finds_before, total_finds_after = calculate_finds(motif_with_country)

# merge finds data into world GeoDataFrame
world = world.merge(total_finds_before, how="left", left_on="ADMIN", right_on="country", suffixes=('', '_before'))
world = world.merge(total_finds_after, how="left", left_on="ADMIN", right_on="country", suffixes=('', '_after'))
world = world.merge(total_finds_all_years, how="left", left_on="ADMIN", right_on="country", suffixes=('', '_all'))

# drop duplicate 'country' columns 
world.drop(columns=['country_after', 'country_all'], inplace=True, errors='ignore')

# fill missing values with 0 for plotting
world['total_finds_all_years'].replace(0, float('nan'), inplace=True)
world['total_finds_before'].replace(0, float('nan'), inplace=True)
world['total_finds_after'].replace(0, float('nan'), inplace=True)

# color palette
palette = sns.color_palette("viridis", as_cmap=True).reversed()
# bins for classifications
boundaries = [1, 5, 10, 15, 20, 50, 100, 200, 600]
# boundary norm to categorize colors
norm = BoundaryNorm(boundaries, palette.N, clip=True)

# plot finds
def plot_finds(gdf, column, title):
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    gdf.boundary.plot(ax=ax, linewidth=1)  # Draw the boundaries

    gdf.plot(column=column, ax=ax, legend=True,
               cmap=palette,
               norm=norm,
               legend_kwds={'label': title, 'orientation': "horizontal"},
               missing_kwds={"color": "lightgrey", "label": "No finds"})
    
    plt.title(title)
    plt.show()


plot_finds(world, 'total_finds_all_years', 'Total Finds by Country (All Years)')
plot_finds(world, 'total_finds_before', 'Total Finds by Country (Before Year 350)')
plot_finds(world, 'total_finds_after', 'Total Finds by Country (After Year 350)')

