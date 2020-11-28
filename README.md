--------Purpose---------------------------------------------------------------
Opposition calculator will take an object ID number, and determine at what
dates, within a date range, that object is at it's brightest apparrent 
magnitude.

This program utilizes the jplhorizons module from astroquery

The backend ephemeris gatherin is completed using the jplhorizons module.
This program compiles the date range, and table settings before the query,
then sorts the returned ephemeris for opposition dates. 

JPL Horizons can be found at https://ssd.jpl.nasa.gov/horizons.cgi


---------- Settings to Use on JPL Horizons--------------------
Necessary inp

-------Instructions for Using Opposition Calculator-----------
1. Run the Program, it will ask for multiple or single objects.
    1.A. IF RUNNING SINGLE OBJECT: You will only need the targets ID number in 
        JPL horizons to determine it's oppositions.
    1.B. IF RUNNING MULTIPLE OBJECTS: You will need a text file (.txt) that 
        contains all of the objects ID numbers in a single column.
            EX: (The text file should be formatted as follows)
            
                12
                178
                1
                168
                11290
        
        The Text file must be saved in the same directory as the program.
                
2. THe Program will ask for the location, and date, and viewing informaiton.
4. It will ask for saving plots or not.
        WARNING: If running more then ~100 objects do not save the plots. Each
            plot is saved as a png file, saving plots slows down the program
            it can also fill up drive space fast with thousands of objects.
5. It will ask either for the ID number or the text file. 
    NOTE: The text file must be saved in the same directory as the program.


--------Output Data---------------
After inputting the ID number or file the program will start parsing each
object. 

oppositions.csv:
    If oppositions are found a CSV title 'oppositions.csv' will be made. 
    This is a table with all of the oppositions for each object. 


plots directory:
    If user elected to save the plots a folder titled "plots" will be made
    and populated with the plot images for each object.



THIS PROGRAM IS NOT COMPLETE. It still a side project used for my own research. 
There are many bugs and it poorly handles crashes. I Hope to make this an 
executable project at some time but I do not currently have the time to fix 
this properly. 



Developed By Justin Germann - jusgermann@gmail.com
	
-- Program is Written in Python 3.8.