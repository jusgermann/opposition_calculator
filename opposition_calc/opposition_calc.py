# -*- coding: utf-8 -*-
from astroquery.jplhorizons import Horizons
from support_files.pre_task import date_checker, location_checker
from support_files.post_task import find_oppositions, airmass_limit, plotter
from pathlib import Path

import pandas as pd

import warnings
import os



"""
Program takes ID number for targets in JPL horizons and determines at what dates
those targets will be at opposiion (i.e. when they'll be at their brightest 
apparent magnitude). 
This aids in determining when those objects will be the eiseist to observe, it's 
particularly handy for dim asteroids. 


Input:
    Individual text inputs or a text document with a single column of object
    ID numbers is excepted. The text document must be stored in the current 
    working directory of this program. 
    
    All other inputs are controlled through text and questions in command line.

Output:
    The program will output a file titled oppositions.csv containing dates of 
    local minimum magnitude that are brighter than the minimuim magnitude cut 
    off. 
    
    If save plot it (y) then a folder titled 'plots' will be created in the 
    current working directory and .png images of magnitude v date will be 
    saved for each object parsed. 
        WARNING: Saving plots will add time and will take up much more storage, 
        it is not recommended to save plots with thousands of asteroids.

NOTE: A few files are required to be included with this program for it to 
function properly. A directory titled "support_files" containing pre_tasks.py
and post_task.py is required. These are python modules taken out of the main 
code to keep the program 'neater'. 
    A list of observatory codes must also be included. This is a text document
titled 'loc_ids.tx'. This must be included unless the location input cannot 
be checked for approval. 

_____________________________________________________________________________
# List of Ephemeris columns to use in final ==================================
 
    (eph['targetname',
        'datetime_str',
       'V',
       'delta',          
       'delta_rate',
        'alpha_true'
        'RA',
        'DEC',
        'airmass'
        ])
_______________________Dictionary of column output names______________________
         {     
          'targetname':'Target Name',
          'datetime_str':'Date-Time (Date__(UT)HR:MN)',
          'V':'V (mag)',
          'RA':'RA (deg)',
          'DEC':'DEC (deg)',
          'delta':'delta (AU)',
          'alpha_true':'True Phase Angle (deg)',
          'airmass' : 'airmass'
           }
        
 =============================================================================
Authored by Justin Germann (MS* Space Studies University of North Dakota)
    -- 701-206-0395
    -- jusgermann@gmail.com
"""


def main():
    """ 
    Main module handles the inputs from the user and setting up the basic
    variables.
    """
    
    print('__________________________________________________________________')
    print('__________________________________________________________________')
     
    # Turn off a warning that is not helpful.
    pd.set_option('chained_assignment', None)
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    # Makes inputs global so other functions can access.
    global target_list                             # check if this is required.
    global location
    global start_date
    global stop_date
    global step_size
    global min_mag
    global column_names
    global save_plot
    global airmass_q
    global airmass_lim
    global skip_day

    
    # Creating empty DF for appending too.
    column_names = ['targetname',
                    'datetime_str',
                    'V',
                    'delta',
                    'alpha_true',
                    'RA',
                    'DEC',
                    'airmass'
                    ]
    
    # For Formating
    print_break = "___________________________\n"
    
    # Question for single or multiple objects
    while True:
        multiple_q = input('''                          
Finding oppositions for Multiple objects (m) or a Single object (s)? \n
Input m or s: ''')
        mul_q_fir = multiple_q[0].lower()                     
        if  mul_q_fir == 'm':
            break
        if  mul_q_fir == 's':
            break
        else:
            print("{}Incorrect Character Input".format(print_break))

    # Uses location_checker module to make sure location is valid.
    location = location_checker()
    
    # Feeds to functions to get dates in correct formats
    while True:
        start_date = date_checker('Start')
        stop_date = date_checker('End')
        
        if stop_date == start_date:
            print("{}Start and End dates cannot be the same"
                  .format(print_break))
        else:
            break
    
    # Question to collect step size input
    while True:
        step_list = ['s', 'm', 'h', 'd', 'y']
        step_size = input('Step size: (ex: 10d, 3m, 2h): ')
         
        if step_size[-1] in step_list:
            break
        else:
            print('{}Input step unit listed: {}'.format(print_break,step_list))
        
        
    # Question to determine the desired magnitude limit.
    while True:
        min_mag = input('Magnitude Limit: ')
        try:
            min_mag = float(min_mag)
            break
        except:
            print("{}Must be integer".format(print_break))
    
    # make it so you can't limit airmass or daylight when step size > 1 day.
    if step_size[-1] != 'd':
        # Question to determine if limit by airmass is desired.
        while True:
            airmass_q = input("""Limit airmass's? y or n: """)
            if airmass_q[0].lower() == 'y':
                airmass_q = True       
                airmass_lim = input("Input Airmass Limit: ")
                
                try:
                    airmass_lim = float(airmass_lim)
                    break
                except:
                    print("{}Must be integer".format(print_break))
            else:
                airmass_q = False
                break
       # Question to see if you wish to skip daylight hours.
        while True:
            skip_day = input('Skip Daylight? y or n: ')
            skip_day = skip_day[0].lower()                     
            if  skip_day == 'y':
                break
            if  skip_day == 'n':
                break
            else:
                print("{}Incorrect Character Input".format(print_break))
    
    # Creates Variables for skipped days.
    else:
        skip_day = 'n'
        airmass_q = 'n'
        print('\n--- NOTICE ---')
        print("Since Step >1 Day\nAirmass cutoff = N\nDaylight cutoff = N")
            
    # Question to check to see if plots wish to be saved.
    while True:
        save_plot = input("Save plot images? (y or n): ")
        save_plot_fir = save_plot[0].lower()                     
        if  save_plot_fir == 'y':
            if mul_q_fir =='m':
                # Second question to confirm when saving multiple plots.
                save_plot = input("""
\n\nIf Parsing 1OO's of objects the plot generation will take up storage
resources and considerably slow the parsing process.
Are you sure you wish to save plots? y or n: """ 
)
                save_plot_fir = save_plot[0].lower()
                if save_plot_fir == 'y':
                    break
                else:
                    print("Not saving plots")
            break
        if  save_plot_fir == 'n':
            break
        else:
            print("{}Incorrect Character Input".format(print_break))
    
    file_organizer(multiple_q)



def file_organizer(multi_single):
    
    # Creats DF with column names for populating.
    opposition_df = pd.DataFrame(columns=column_names)    

    # Check if Single or multiple objects.
    if multi_single == 'm':
        opposition_df, count, not_tar_count = multi_obj(opposition_df)

        
    if multi_single == 's':
        opposition_df, count, not_tar_count = sin_obj(opposition_df)

    # Re-arrange columns since concat screws them up.
    cols = ['targetname', 
            'datetime_str', 
            'V', 
            'RA', 
            'DEC', 
            'delta', 
            'alpha_true',
            'airmass'
            ]
    
    opposition_df = opposition_df[cols]
    
    # Retrieving line count == Amount of oppositions found.
    total_opp = opposition_df.V.count()
    
    # Re-name columns to include Units.
    col_dict = {
                'targetname':'Target Name',
                 'datetime_str':'Date-Time (Date__(UT)HR:MN)',
                 'V':'V (mag)',
                 'RA':'RA (deg)',
                 'DEC':'DEC (deg)',
                 'delta':'delta (AU)',
                 'alpha_true':'True Phase Angle (deg)',
                 'airmass': 'airmass'
                 }
    
    opposition_df = opposition_df.rename(columns = col_dict)
    
    #Saving final Concatted dataframe to csv.
    opposition_df.to_csv((os.path.join(os.pardir, 'opposition.csv')), 
                        index=False)
    

    print('''
\n\n{} Opposition Dates have been found in {} ephemeris('s).'''
                                                    .format(total_opp, count))

    if not_tar_count != 0:
        print('''{} object(s) ID number's were not found in JPL Horizons database.
              '''.format(not_tar_count))

    if total_opp != 0:
        print('''
Oppositions dates have been saved too oppositions.csv within the directory 
for this program.'''
)
    else:
        print('No oppositions found with specified parameters.')
    
    

def obj_query(identifier, 
              location, 
              start_date, 
              stop_date, 
              step_size, 
              min_mag,
              ):
    """ Responsible for pulling ephemeris information from JPL Horizons"""

    # Calls object identified with date information from JPL horizons.    
    obj = Horizons(id=identifier, location=location,
                   epochs={'start':start_date,
                           'stop':stop_date,
                           'step':step_size},                     
                   )

    # Checks if Daylight needs to be skipped
    if skip_day == 'y':
        # Creating Ephemeris without daylight hours
        eph = obj.ephemerides(skip_daylight=True)
    else:
        # Creating ephemeris object at all hours
        eph = obj.ephemerides(skip_daylight=False)  
    
     
    # Convert table to pandas dataframe (easier to manipulate).
    eph_df = eph[column_names].to_pandas()
    
    # Removes objects with airmass higher then limit
    if airmass_q == True:
        eph = airmass_limit(eph_df, airmass_lim)
    
    # Check if Plots need to be saved before editing dataframe.
    if save_plot[0].lower() == 'y':
        plotter(eph_df, identifier, min_mag)
    else:
        pass
        
    # Uses find oppositions to find opposition dates.
    min_eph_df = find_oppositions(min_mag, eph_df)

    return min_eph_df



def multi_obj(opposition_df):
    
    print("""
___________________________\n
Text file containing object ID's in column required.""")

    # Opens text file with asteroid ID's to parse
    while True:
        # Input for finding file name
        file_name = input("""
Input text file name containing object ID's
Include .txt file extension (ex: asteroid.txt): """)
        try:
            # Make sure the directory is good and open the file.
            path = os.getcwd()
            obj_file = os.path.abspath(os.path.join(path, os.pardir, file_name))

            # Open file
            with open(obj_file, 'r') as target_list:
                targets = target_list.read().split('\n')
                
            break
        except:
            print('________________________\nFile not found, check file name.')
    
    # Start new count
    count = 0
    not_tar_count = 0
    
    # check if ID's are number, if not remove them
    for target in targets:       
        count=count + 1
        
        try:
            int(target)
            print("-- Parsing obj #{}: Object ID: {} --".format(count, target))
            
            # Retrieving ephemeris from JPL_Horizons and getting local min.
            min_eph_df = obj_query(target, 
                                   location, 
                                   start_date, 
                                   stop_date, 
                                   step_size, 
                                   min_mag
                                   )               
            # Concat's object to dataframe after each loop
            frames = [opposition_df, min_eph_df]
            opposition_df = pd.concat(frames, sort=True)
        
        except:
            not_tar_count = not_tar_count + 1
            targets.remove(target)
            print("""Target with the ID of '{}' removed, as it was not an ID number"""
                  .format(target))
    
        
    return opposition_df, count, not_tar_count
    

    
def sin_obj(opposition_df):
    
    
    target = input('Input Object Identifier: ')
    print('-- Parsing Obj ID: {} --'.format(target))

    # Retrieving ephemeris from JPL_Hor and getting local min.
    try:
	    min_eph_df = obj_query(target, 
	                           location, 
	                           start_date, 
	                           stop_date, 
	                           step_size, 
	                           min_mag
	                           )
    except:
    	print(
"""No ephemeris meets criteria. Check table cut-off values shown above for:
 
	elevation angle
  	airmass
  	daylight only
  	solar elongation
  	local hour angle
  	RA/DEC angular rate
  				""")
    
    frames = [opposition_df, min_eph_df]
    opposition_df = pd.concat(frames)
       
    count = 1
    not_tar_count = 0

    return min_eph_df, count, not_tar_count



if __name__ == '__main__':
    main()