'''Second version of a finder chart creator that uses Aladin to locate stars. Reads
in a csv file with given name, RA, and DEC of the user's target list. Returns .jpg
images of the finder chart for each given object in the csv file.

This version prompts the user to enter her desired values from the command line. 
It asks the user for the file name, the color band, and the amount of zoom desired.

Download for Aladin Desktop can be found here: 
http://aladin.u-strasbg.fr/java/nph-aladin.pl?frame=downloading 

FORMAT OF CSV:
- First line is assumed to be a header and is omitted during read-in. Later 
  versions will include a dialogue so the user may specify whether or not she 
  would like to skip the first line.
- The first column should be the name of the target; the second should be the RA 
  of the target, and the third should be the Dec of the target (the way that I 
  skip the first line is a bit janky. Stackoverflow was surprisingly unhelpful 
  in terms of finding a different method. 

Other notes:
- Spaces in names of objects are parsed out
- Any parenthesis that exist in DEC are also parsed out. This is because Excel 
  doesn't like cells that start with + or -, so the user may have included these 
  parenthesis
- Works with Aladin v8.0. Has not been tested with other versions.
- Takes approximately 7 seconds per target on my Mac, which has an i5 processor
  and 8 GB of RAM.
- Currently only works on Mac. Working on making it run on Linux machines as 
  well.

................................................................................
'''
import csv
import subprocess
import time

# Specifies the path to Aladin app, and most importantly the .jar file. This
# should work for any Mac, as long as you have Aladin installed in your 
# Applications folder. 
path = 'java -jar /Applications/Aladin.app/Contents/Java/Aladin.jar'

def get_file_name():
    while True:
        try:
            file_name = raw_input('Enter the name of the .csv file: ')
            file = open(file_name)
            break
        except IOError:
            print("Error: improper file type or missing file.")
    return file_name

class FormatInError(Exception):
    #raised when an improper value is passed for the color band
    pass


def get_color_band():
    color_band = "" 
    while True:
        try:
            color_band = raw_input('Enter either "H", "K",  ' +
            'or "color" for the desired band: ')
            if color_band == "H" or color_band == "K" or color_band =="color":
                break
            else:
                raise FormatInError 
        except FormatInError:
            print('Improper format!')
    return color_band

def get_zoom_type():
    while True:
        try:
            zoom_type = raw_input('State whether "degree", "arcmin", or ' +
            '"arcsec" is desired for the frame: ')
            if zoom_type == "degree" or zoom_type == "arcmin" or zoom_type == "arcsec":
                break
            else:
                raise FormatInError 
        except FormatInError:
            print('Improper format!')
    return zoom_type

def get_zoom_value():
    while True:
        try:
            zoom_value = raw_input('State an integer value for how many degrees, ' +
            'arcminutes, or arcseconds are desired for the zoom: ')
            float(zoom_value)
            break
        except ValueError:
            print('Not an integer!')
    return int(zoom_value)
        

def get_variables():
    global file_name
    global color_band
    global zoom
    global zoom_type
    global zoom_value
    file_name = get_file_name()
    color_band = get_color_band()
    zoom_type = get_zoom_type()
    zoom_value = get_zoom_value()
    return str(zoom_type), str(zoom_value)


def read_csv_file():
    csv_file_name = open(file_name) 
    csv_file = csv.reader(csv_file_name)
    csv_cat(csv_file)

def csv_cat(csv_file):
    global coordinates
    global names
    coordinates = []
    names = []
    i = 0
    for row in csv_file:
        # "if" statement is my way to skip the first line. Would like to change this.
        if i != 0:
            # creates name array
            names.append(row[0].replace(" ", ""))
            # reads and parses parenthesis from declination
            dec = row[2]
            dec = dec.replace("(", "") 
            dec = dec.replace(")", "")
            # appends RA and declination to be read by Aladin
            coordinates.append(row[1] + ' ' + dec)
        i = 1

# Spawns new process. "stdin" specifies standard input of executed program 
def spawn_process(units, zoom):
    global p 
    p = subprocess.Popen([path],
        shell=True,
        stdin=subprocess.PIPE)
    # Send data to standard input of program
    p.stdin.write('grid on\n')
    send_coordinates(units, zoom)


def send_coordinates(units, zoom):
    # Again, the p.stdin.write sends values to the standard inputs of Aladin
    j = 0
    space = "_"
    print(coordinates)
    for obj in (coordinates):
        name = names[j]
        p.stdin.write('reset; get hips(P/2MASS/'+color_band+') '+obj+'; \n')
        title = name + "_" +  zoom + units
        # Zoom can be changed by the user.
        p.stdin.write('zoom '+zoom+'; save '+title+'.jpg\n')
        j = j + 1

if __name__ == "__main__":
    start_time = time.time()
    units, num = get_variables()
    read_csv_file()
    spawn_process(units, num)
    p.stdin.write('quit\n')
    p.wait()
    print("--- %s seconds ---" % (time.time() - start_time))
