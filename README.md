# README: Early Christian Art on Roman Epitaphs
This project was developed as part of the 2024 course 'Computational literacy for the humanities and social sciences' at the University Helsinki.

## Project Overview
This project examines figural decoration on early Christian epitaphs to understand whether a distinct Christian iconography emerges in this context. What kind of figural decoration can be found on early Christian epitaphs? Is there a Christian iconography similar to early Christian art in other funerary contexts (e.g., Roman catacombs, late Roman sarcophagi)?
(For a short introduction into the develompent and timeframe of early christian art see: https://www.britannica.com/art/Early-Christian-art)

The analysis uses data from the **Epigraphic Database Heidelberg (EDH)**, focusing on inscriptions labeled as Christian. Since the EDH does not categorize figural representations, the project employs keyword-based searches to identify relevant descriptions from the free-text commentary section. 

## Data Sources
- **Epigraphic Database Heidelberg (EDH)**: Provides Latin and bilingual (Latin-Greek) inscriptions of the Roman Empire.
- **Keyword List**: Derived from a PhD study on figural depictions on "loculus-slabs" found in early-christian catacombs in Rome (https://archiv.ub.uni-marburg.de/diss/z2012/0956/pdf/dee.pdf). 


## Project Files

### Code Files
1. **`api_client.py`**: Script for interacting with the EDH API to download the relevant data.
2. **`keyword_filter_regex.py`**: Implements keyword filtering using regular expressions to identify mentions of figural depictions in the commentary section of dataset.
3. **`keyword_filter_stanza.py`**: A script that utilizes the Stanza NLP library to filter keywords from the dataset. Although it was initially developed, it was later discarded due to the lengthy processing time required for lemmatization on the large dataset. It is retained solely for documentation purposes.
4. **`keyword_analysis.py`**: Performs analysis of the filtered data, including frequency analysis, chronological trends, and geographical distribution.

### Data Files
1. **`filtered_data.csv`**: CSV version of the filtered data.
2. **`filtered_data.json`**: JSON version of the filtered data.
3. **`results.json`**: Final results of the data analysis.

### Configuration Files
1. **`keywords.txt`**: A list of keywords used for identifying figural elements in free-text descriptions.
2. **`keyword_groups.txt`**: Categorized groups of keywords (e.g., biblical scenes, symbols, other motifs).

### Dependencies
- **`requirements.txt`**: Specifies the Python libraries required to run the project.

### Auxiliary Files
- **`__init__.py`**: Marks the directory as a Python module.
- **`mapdata/`**: Directory for storing files that help mapping the geographical distribution of figural depictions downloaded from https://www.naturalearthdata.com
- **`__pycache__/`**: Directory containing compiled Python files.

## Workflow

1. **Data Extraction**
   - Use `api_client.py` to query the EDH API and download relevant data. The fetched dataset is stored in `results.json`

2. **Data Cleaning and Keyword Filtering**
    Key Features of `keyword_filter_regex.py`:
    - Loading the Dataset: Reads the results.json file and converts it into a Pandas DataFrame.
    - Filtering: Excludes pagan entries and rows without commentary text.
    - Keyword Matching: Loads a list of keywords from `keywords.txt` and creates regex patterns to match variations of these keywords in the commentary text. Uses Stanza NLP for lemmatization to standardize variations of words.
    - Motif Grouping: Assigns motifs to predefined groups from `keyword_groups.txt`.
    - Marking Christian Items: Flags entries as christian based on specific criteria 
    Results:
    - The cleaned and filtered data is stored in `filtered_results.json`.

3. **Data Analysis**
    The analysis of the filtered data is implemented `keyword_analysis.py` and reads the data of `filtered_results.json`.
    Frequency Analysis:
    - Counts occurrences of specific motifs. Analyzes the most common motifs, motif groups, and motifs that are identified as christian motifs. Plot frequency distributions using bar plots.
    Chronological Trends:
    - Analyzes changes in iconography over time. Groups data into 50-year time bins and visualizes trends using line plots and heatmaps.
    Geographical Distribution:
    - Maps motifs to their geographical find spots. Visualizes the geographical distribution of the most common motifs using world maps, with separate maps for finds before and after 350 CE.

4. **Results**
    For a discussion of the results see `ProjectSummary.pdf`

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scripts**
   - Extract data: `python api_client.py`
   - Filter data: `python keyword_filter_regex.py`
   - Analyze data: `python keyword_analysis.py`





