## Purpose

Opposition calculator will take an object ID number, and determine at what
dates, within a date range, that object is at it's brightest apparrent 
magnitude.

This program utilizes the atroquery.jplhorizons module. Documentation found 
here https://astroquery.readthedocs.io/en/latest/jplhorizons/jplhorizons.html.

The back end ephemeris gathering is completed using the jplhorizons module.
This program asks for the date range, and table settings before the query,
then mulls through the returned ephemeris for opposition dates. 

JPL Horizons can be found at https://ssd.jpl.nasa.gov/horizons.cgi


## Instructions for Using Opposition Calculator
1. Run the Program, it will ask for multiple or single objects.
    1. **IF RUNNING SINGLE OBJECT:** You will only need the targets ID number in 
        JPL horizons to determine it's oppositions.
    2. **IF RUNNING MULTIPLE OBJECTS:** You will need a text file (.txt) that 
        contains all of the objects ID numbers in a single column.
            
    EX: (The text file should be formatted as follows)
            
        12
        578
        1
        8268
        11290
    
    _The Text file must be saved in the same directory as the program._
                
2. The Program will ask for the location, and date, and viewing information.
3. It will ask for saving plots or not.
        
**WARNING:** If running more then ~100 objects do **not** save the plots. Each
plot is saved as a .png file, saving plots slows down the program
it can also fill up drive space fast with thousands of objects.

4. It will ask either for the ID number or the text file. 

_NOTE:_ The text file must be saved in the same directory as the program.


## Output Data

After inputting the ID number or file the program will start parsing each
object. 

oppositions.csv:

* If oppositions are found a CSV title 'oppositions.csv' will be made. 
This is a table with all of the oppositions for each object. 


plots directory:

* If user elected to save the plots a folder titled "plots" will be made
and populated with the plot images for each object.



**THIS PROGRAM IS NOT COMPLETE.** It is a side project used for my own research. 
There are many bugs and it poorly handles crashes. I Hope to make this an 
executable project at some time but I do not currently have the time to fix 
this properly. 



Developed By Justin G. - jusgermann@gmail.com
	
This program is written in Python 3.8.
