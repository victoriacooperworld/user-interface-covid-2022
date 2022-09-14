#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun 24th, 2022
@author: Victoria Niu
"""

import csv
import datetime
from mimetypes import init
import os
import pandas as pd
import numpy as np
from Bio import SeqIO
import collections
from pip import main
from scipy import stats
from statsmodels.sandbox.stats.multicomp import multipletests
import main

if __name__ == '__main__':

    dir = r"F:\OutputFiles\TetramerID\Merged\Merged\Merged"
    st = datetime.datetime.now()



    #Process_MergeTxt(dir, deleteOriginals=False)
    main.Process_MergeTxt(dir)
    et = datetime.datetime.now()
    timetotal = et-st
    print("Total time taken was ", timetotal)
