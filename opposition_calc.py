# -*- coding: utf-8 -*-
from astroquery.jplhorizons import Horizons
from matplotlib import pyplot as plt

import matplotlib as mpl
import numpy as np
import pandas as pd

import warnings
import os



"""
Module takes inputs of ID numbers from the user to produce opposition dates 
for objects in JPL Horizons.

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
        NOTE: Saving plots will add time and will take up much more storage, 
        it is not recommended to save plots with thousands of asteroids.

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
_________________________List of column output names__________________________    
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
          
    TODO:
        - Add a list of locations and create a while loop to check for bad 
        location inputs.
        
 =============================================================================
Authored by Justin Germann (MS* Space Studies University of North Dakota)
    -- 701-206-0395
    -- jusgermann@gmail.com
"""


def main():
    
    print('__________________________________________________________________')
    print('__________________________________________________________________')
     
    # Turn off a warning that is not helpful.
    pd.set_option('chained_assignment', None)
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    # Makes inputs global so other functions can access.
    global target_list
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
    
    # Defining Gobal vars through input 
    
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


    location = input('Location ID (Mauna Kea = 568): ')
    
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
            
    # Question to check to see if plots wish to be saved.
    while True:
        save_plot = input("Save plot images? (y or n): ")
        save_plot_fir = save_plot[0].lower()                     
        if  save_plot_fir == 'y':
            if mul_q_fir =='m':
                # Second question to confirm when saving multiple plots.
                save_plot = input("""
\n\nIf Parsing many objects the plot generation will take up storage resources
\nand considerably slow the parsing process. \n
Are you sure you wish to save plots? y or n: 
                      """ )
                save_plot_fir = save_plot[0].lower()
                if save_plot_fir == 'y':
                    break
                else:
                    print("{}Incorrect Character Input".format(print_break))
            break
        if  save_plot_fir == 'n':
            break
        else:
            print("{}Incorrect Character Input".format(print_break))
    
    file_organizer(multiple_q)



def date_checker(start_end):
    # Create list for acceptible month and day integers
    month_nums = []
    day_nums = []

        
    # Loop for getting input dates
    while True:
        
        for i in range(1,13):
            month_num = '%0.2d' % i 
            month_nums.append(month_num)
        
        for i in range(1,32):
            day_num = '%0.2d' % i
            day_nums.append(day_num)
        
        # Creates input with correct grammer for start or end statements.
        date = input('{} date yyyy-mm-dd: '.format(start_end))
        
        # If month with 30 days the 31 is deleted from day's list.
        month_inp = date[5:7]
        
        if month_inp in ['04', '06', '09', '11']:
            day_nums = day_nums[:-1]
        
        # Checks that year is valid
        try: 
            int(date[:4])
        except:
            print('Year Input is not formated correctly.')
            
        # Chekcs for leap years
        in_year = int(date[:4])
        if in_year % 4 == 0 and in_year % 100 != 0:
            leap_year = True
        elif in_year % 100 == 0:
            leap_year = False
        elif in_year % 400 == 0:
            leap_year = True
        else:
            leap_year = False
        
        # If 2nd month assigns days depending on leap year.            
        if month_inp == '02':
            if leap_year == True:
                day_nums = day_nums[:-2]
            if leap_year == False:
                day_nums = day_nums[:-3]
        
        # Checks for dashes
        if date[4] and date[7] != '-':
            print('Input yyyy-mm-dd with dashes in correct location.')
        
        # Checks if years are within JPL's range
        if start_end == 'start':
            int(date[:4]) < 1599
            print('No Dates prior to 1599, {} is out of range'.format(date))

        # Checks month integer is valid
        if date[5:7] not in month_nums:
            print("Month date input was out of range, must be 01-12")
     
        # Checks if day integer is valid
        if date[8:] not in day_nums:
            print("""Month {} has {} days, input day was out of range."""
                  .format(month_inp, day_nums[-1]))
        else: 
            break
        
    return date

            
        

def file_organizer(multi_single):
    
    # Creats DF with column names for populating.
    opposition_df = pd.DataFrame(columns=column_names)    

    # Check if Single or multiple objects.
    if multi_single == 'm':
        opposition_df, count, not_tar_count = multi_obj(opposition_df)

        
    if multi_single == 's':
        opposition_df, count, not_tar_count = sin_obj(opposition_df)

    # Re-arrange columns as concat screws them up.
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
    opposition_df.to_csv('oppositions.csv',index=False)
    

    print('''
\n\n{} Opposition Dates have been found in {} ephemeris('s).'''
                                                    .format(total_opp, count))

    if not_tar_count != 0:
        print('''{} object(s) ID number's were not found in JPL Horizons database.
              '''.format(not_tar_count))

    if total_opp != 0:
        print('''
Oppositions dates have been saved too oppositions.csv\n
within the directory for this program.
                  ''')
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
        eph = airmass_limit(eph_df)
    
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
            with open(file_name, 'r') as target_list:
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
    min_eph_df = obj_query(target, 
                           location, 
                           start_date, 
                           stop_date, 
                           step_size, 
                           min_mag
                           )
    
    frames = [opposition_df, min_eph_df]
    opposition_df = pd.concat(frames)
       
    count = 1
    not_tar_count = 0

    return min_eph_df, count, not_tar_count



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



def airmass_limit(eph):
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



if __name__ == '__main__':
    main()