# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 19:29:30 2020

@author: Owner
"""

import os
import glob
import json
from getpass import getpass

from tqdm import tqdm
from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", getpass()))