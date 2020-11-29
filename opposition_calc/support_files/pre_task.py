"""
This file handles modules for any tasks that takes place before the ephemeris 
creation.
"""


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
            
        # Checks for leap years
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



def location_checker():
    """Module checks with a  list of known observatories.
    A text file titled loc_ids.txt MUST be included in support_files directory.
    Returns the ID number that the user inputed"""



    # Opens text file of location ID's and saves to contents.
    with open('support_files/loc_ids.txt') as loc_ids:
        contents = loc_ids.read()
        while True:
            # Asking for the location ID.
            loc_in = input('Location ID (Mauna Kea = 568): ')
            
            # Two different responses depending if the input was valid.
            if loc_in in contents:
                print('Location {} Selected.'.format(loc_in))
                break
            else:
                print(
"""Location ({}) is NOT valid.
See   https://ssd.jpl.nasa.gov/horizons.cgi#top   for list of locations.
""".format(loc_in))
                continue
            
    return loc_in      
        
                  

    