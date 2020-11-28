from matplotlib import pyplot as plt

import os

import numpy as np
import matplotlib as mpl



"""
This file handles modules for any tasks that takes place after the ephemeris 
creation.
"""

def find_oppositions(min_mag, obj_df):
    """
    Removes all rows with a magnitude lower than the specified magnitude from 
    the dataframe. Finds the local minimums of the magnitude.
    
    RETURNS: A dataframe containing only dates that are oppositions below the
    min_mag threshold
    """
    # Checks the mag against min_mag, creates a new DF with dates brighter
    min_obj_df = obj_df[obj_df.V < min_mag]
    
    # adds local min specified minimum to a temporary dataframe
    min_obj_df['local_min'] = min_obj_df.V[(min_obj_df.V.shift(1) >=
                    min_obj_df.V) & (min_obj_df.V.shift(-1) >= min_obj_df.V)]

    
    try:
        # Checks the last and the first line for local min
        first_line = min_obj_df.iloc[0]
        second_line = min_obj_df.iloc[1]
        if first_line.V <= second_line.V:
            min_obj_df.iloc[0, -1] = 'XX'
            
        last_line = min_obj_df.iloc[-1]
        second_last_line = min_obj_df.iloc[-2]
        if last_line.V <= second_last_line.V:
            min_obj_df.iloc[-1, -1] = 'XX'
    
        # Removes all row's that are not local min's
        min_obj_df['local_min'].replace('', np.nan, inplace=True)
        min_obj_df.dropna(subset=['local_min'], inplace=True)
        min_obj_df = min_obj_df.drop('local_min', 1)
    except:
        pass

    return min_obj_df   



def airmass_limit(eph, airmass_lim):
    """"Removes any rows that do not match airmass limit."""
    
    # Get Airmass location that are higher then the limit
    high_airmass_index = eph[eph['airmass'] > airmass_lim].index
    
    eph.drop(high_airmass_index, inplace=True)
    
    return eph

    

def plotter(obj_df, tar_name, min_mag):
    """
    Plots the magnitude overtime of each asteroid. Along with line at the 
    magnitude limit.
    """
    
    # Creates a directory to save output data, within cwd
    save_path = os.path.join(os.getcwd(), 'plots')
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        
    mpl.style.use('seaborn')
    obj_df['min_mag'] = min_mag
    
    ax = obj_df.plot(x='datetime_str', 
                     y=['V','min_mag'],
                     rot=90,
                     title='{}'.format(tar_name))
    
    ax.legend().remove()
    ax.set_ylabel('Magnitude')
        
    plt.savefig(os.path.join(save_path, '{}.png'.format(tar_name)),
                bbox_inches='tight')
    plt.close()
