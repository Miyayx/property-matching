#!/bin/bash

python replace_label_data.py
python del_special.py
python filter_special.py
python match.py
python del_once.py
