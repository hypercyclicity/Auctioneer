#!/bin/bash 

sqlite3 auction.db < create_table

python adder.py
