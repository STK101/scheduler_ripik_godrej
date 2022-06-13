import pandas as pd
import numpy as np
import argparse
import tp_updater

def parse_args():
    parser = argparse.ArgumentParser(description='Transition Probability Updater')
    parser.add_argument('--bpr',type=str,required=True,help="Path to the historic daily bpr")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    hist_data = tp_updater.update_transition_probabilities(args.bpr)
    hist_data.to_csv('hist_data.csv')
