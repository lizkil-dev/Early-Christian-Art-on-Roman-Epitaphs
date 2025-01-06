import pandas as pd
import json
import stanza
import re


#initialize stanza
# stanza.download('de')
nlp = stanza.Pipeline('de')


#load dataset
with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

items = data['items']
df = pd.json_normalize(items)

# Remove items marked as pagan
df = df[df['religion'] != "names of pagan deities; cult functions, pagan"]

# Remove items without commentary
df = df[df['commentary'].notna() & (df['commentary'].str.strip() != '')]

# load keyword-list
with open('keywords.txt', 'r', encoding='utf-8') as keyword_file:
    keywords = [line.strip() for line in keyword_file.readlines() if line.strip()]

# load list of to be excluded phrases
#with open('excluded_phrases.txt', 'r', encoding='utf-8') as phrase_file:
#    excluded_phrases = [line.strip() for line in phrase_file if line.strip()]

keywords_set = set(keywords)

# Search for keywords in commentary column
def find_motifs_and_filter(commentary):
    if isinstance(commentary, str):
        
        # Remove excluded phrases
        #for phrase in excluded_phrases:
        #    commentary = commentary.replace(phrase, "")

        motifs = set()

        # Extract nouns from commentary
        doc = nlp(commentary)
        nouns = [
            word.lemma for sentence in doc.sentences for word in sentence.words if word.upos == "NOUN"
        ]

        # Match lemmas with keywords
        for noun in nouns:
            if noun in keywords_set:  
                motifs.add(noun)

        if motifs:
            return ', '.join(sorted(motifs))  
    return None

# Apply the function to the commentary column
df['motifs'] = df['commentary'].apply(find_motifs_and_filter)

# Filter dataset to show only items with motifs
df = df[df['motifs'].notnull()]

# Convert to JSON
df.to_json('filtered_data.json', orient='records', lines=False, force_ascii=False)

# Make JSON pretty
with open('filtered_data.json', 'r', encoding='utf-8') as f:
    filtered_data = json.load(f)

with open('filtered_data.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"Length of filtered filtered_data: {len(filtered_data)}")
print(df[['commentary', 'motifs']])


