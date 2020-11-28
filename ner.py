# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import glob
import json

from tqdm import tqdm
from transformers import pipeline


model = pipeline('ner', use_fast=True, grouped_entities=True)

doc = "John Smith went to the store in the United States."*5
entities = model(doc)

#changing as a test
# entities = [x if i>0 else {'entity_group': 'ORG', 'score': 0.9888544976711273, 'word': 'John Smith'} for i, x in enumerate(entities)]

#de-duplicating can be done in neo4j (ideally append offsets)

maindir = 'C:\\Users\\Owner\\Desktop\\enron\\data'
outdir = os.path.join(maindir, 'processed')
if not os.path.isdir(outdir):
    os.mkdir(outdir)

# divide it into sections so we can experiment in the meantime
files = [x for x in glob.glob(os.path.join(maindir, 'extracted', '**'), recursive=True) if not os.path.isdir(x)]
processed_files = [os.path.split(x)[-1] for x in glob.glob(os.path.join(outdir, '**'), recursive=True) if not os.path.isdir(x)]
to_process = [x for x in files if os.path.split(x)[-1] not in processed_files]
for file in tqdm(to_process[:1e5]):
    with open(file, 'rb') as fb:
        doc = json.load(fb)
    doc['entities'] = [x for x in model(doc['body']) if not x['word'].startswith('##')]
    
    with open(file, 'w') as fb:
        json.dump(doc, fb, indent=4)