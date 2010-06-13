#!/bin/bash

python create_mapper_input_data.py | python mapper.py  | python reducer.py 
