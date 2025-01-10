import pandas as pd
import json
import re
import stanza

# Initialize Stanza pipeline
nlp = stanza.Pipeline('de', processors='tokenize,mwt,pos,lemma')

#load json dataset
with open('data/results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

items = data['items']

# convert to a DataFrame
df = pd.json_normalize(items)

# remove items marked as pagan
filtered_df = df[df['religion'] != "names of pagan deities; cult functions, pagan"]

# Remove items without commentary
df = df[df['commentary'].notna() & (df['commentary'].str.strip() != '')]

# Load keywords 
with open('keywords.txt', 'r', encoding='utf-8') as keyword_file:
    keywords = [line.strip() for line in keyword_file.readlines() if line.strip()]

# Generate regex patterns for keywords
patterns = [rf'\b{keyword}(?:e|es|en|n|s)?\b' for keyword in keywords]
combined_pattern = re.compile('|'.join(patterns), re.IGNORECASE)

# Baseform mapping for "special" words 
baseform_mapping = {
    "Delfin": "Delphine",
    "Delfine": "Delphine",
    "Delfinen" "Delphine"
    "Delfins": "Delphine",
    "Delphin": "Delphine",
    "Delphins": "Delphine",
    "Vögel": "Vogel",
    "Bäume": "Baum",
    "Früchte": "Frucht",
    "Lämmer": "Lamm",
    "Kantharoi": "Kantharos",
    "Orant": "Orans",
    "Orans": "Orans",
    "Orantin": "Orans",
    "Oranten": "Orans",
    "Orante": "Orans",
    "Christusmonogram": "Christusmonogramm", 
    "Christusmonogramms": "Christusmonogramm", 
    "Christusmonogramme": "Christusmonogramm", 
    "Christogram": "Christusmonogramm", 
    "Christograms": "Christusmonogramm", 
    "Christogramm": "Christusmonogramm",
    "Christogramme": "Christusmonogramm",
    "Staurogram": "Staurogramm", 
    "Kreuzzeichen": "Kreuz",
    "ascia": "Ascia",
    "Ω": "Alpha & Omega",
    "ω": "Alpha & Omega",
    "Alpha": "Alpha & Omega", 
    "Omega": "Alpha & Omega",
    "alpha": "Alpha & Omega", 
    "omega": "Alpha & Omega", 
    "Girland": "Girlande",
    "Efeurank": "Efeuranke",
    "Weinrank": "Weinranke", 
    "Zang": "Zange", 
    "Zimmermanns": "Zimmermann", 
    "Olivenbaums": "Olivenbaum", 
    "Olivenbaumes": "Olivenbaum"
}

# Load keyword groups from external file
def load_keyword_groups(file_path):
    keyword_groups = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            group_name, motifs = line.split(":", 1)
            keyword_groups[group_name.strip()] = [motif.strip() for motif in motifs.split(",")]
    return keyword_groups

keyword_groups = load_keyword_groups('keyword_groups.txt')

# Reverse the mapping to easily find the group for each motif
motif_to_group = {motif: group for group, motifs in keyword_groups.items() for motif in motifs}

# search for motifs in commentary-column
def find_motifs_and_filter(commentary):
    if isinstance(commentary, str):
        matches = re.findall(combined_pattern, commentary)
        lemmatized_motifs = set()
        motif_groups_found = set()
        
        for match in matches:
            # lemmatize matches 
            doc = nlp(match)
            for sentence in doc.sentences:
                for word in sentence.words:
                    lemma = word.lemma
                    # map to baseform if necessary
                    final_motif = baseform_mapping.get(lemma, lemma)
                    lemmatized_motifs.add(final_motif)
                    # Add the group if the motif is mapped to a group
                    if final_motif in motif_to_group:
                        motif_groups_found.add(motif_to_group[final_motif])

          
        # return sorted motifs as a comma-separated string
        if lemmatized_motifs:
             return {
                'motifs': ', '.join(sorted(lemmatized_motifs)),
                'motif_group': ', '.join(sorted(motif_groups_found))
            }
    
    return None 

# run find_motifs and create new column 'motifs' and 'motif_group'
results = df['commentary'].apply(find_motifs_and_filter)
df['motifs'] = results.apply(lambda x: x['motifs'] if x else None)
df['motif_group'] = results.apply(lambda x: x['motif_group'] if x else None)

# filter only rows with motifs
filtered_df = df[df['motifs'].notnull()]
print(len(df))

# mark items as christian 
def add_christian_column(filtered_df):
    # Define criteria for determining if a result is Christian
    religion = [
        "cult functions, Jewish/Christian",
        "Judaism / Christianity"
    ]
    motifs = [
        "Christusmonogramm",
        "Kreuz",
        "Alpha & Omega",
        "Staurogramm"
    ]

    religion_mask = filtered_df['religion'].isin(religion)
    
    motive_mask = filtered_df['motifs'].str.contains('|'.join(motifs), na=False)

    # Combine both masks to determine if the result is Christian
    filtered_df.loc[:, 'christian'] = (religion_mask | motive_mask).replace({True: "yes", False: "no"})
    
    return filtered_df

# Add the 'christian' column to dataset
filtered_df = add_christian_column(filtered_df)

# Print the count of Christian items
christian_count = filtered_df['christian'].value_counts().get("yes", 0)
print(f'Number of Christian items: {christian_count}')

# save new data to a JSON file
filtered_df.to_json('data/filtered_data.json', orient='records', lines=False, force_ascii=False)

# pretty print JSON
with open('data/filtered_data.json', 'r', encoding='utf-8') as f:
    filtered_data = json.load(f)

with open('data/filtered_data.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

# Save to CSV
# filtered_df.to_csv('data/filtered_data.csv', index=False)