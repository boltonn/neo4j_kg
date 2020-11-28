# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 14:45:06 2020

@author: Owner
"""

import os
import glob
import email
import hashlib
import json

from tqdm import tqdm

maindir = 'C:\\Users\\Owner\\Desktop\\enron\\data'
files = [x for x in glob.glob(os.path.join(maindir, 'raw', '**'), recursive=True) if not os.path.isdir(x)]
    

def extract_email(infile):
    """Parse an email"""
    with open(infile, 'rb') as fb:
        msg = fb.read()
    md5 = hashlib.md5(msg).hexdigest()
    msg = email.message_from_bytes(msg)
    
    #we're just going to ignore encoding issues
    out = {k:v for k,v in msg.items() if isinstance(v, str)}
    out['md5'] = md5
    
    if 'To' in out:
        out['To'] = out['To'].split(',')

    # remember every email can reference past emails so extra work can be done to parse subject lines or separate
    out['body'] = ''.join([part.get_payload() for part in msg.walk() if part.get_content_type()=='text/plain'])

    return out
    
outdir = os.path.join(maindir, 'extracted')
if not os.path.isdir(outdir):
    os.mkdir(outdir)

for infile in tqdm(files):
    out = extract_email(infile)
    with open(os.path.join(outdir, f"{out['md5']}.json"), 'w') as fb:
        json.dump(out, fb)
