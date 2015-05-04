'''First version of a finder chart creator that uses Aladin to locate stars. Reads
in a csv file with given name, RA, and DEC of the user's target list. Returns .jpg
images of the finder chart for each given object in the csv file.

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

................................................................................
'''
import csv
import subprocess

# Specifies the csv file to be read, and sets this file to variable
file = open('Boyer_targets_ordered.csv')
csv_file = csv.reader(file)

# Initalizes dynamic arrays for both names and RA Dec coordinates
names = []
coordinates = []

# Specifies the path to Aladin app, and most importantly the .jar file. This
# should work for any Mac, as long as you have Aladin installed in your 
# Applications folder. 
path = 'java -jar /Applications/Aladin.app/Contents/Java/Aladin.jar'

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
p = subprocess.Popen([path],
    shell=True,
    stdin=subprocess.PIPE)

# Send data to standard input of program
p.stdin.write('grid on\n')

j = 0

# Again, the p.stdin.write sends values to the standard inputs of Aladin
for obj in (coordinates):
    name = names[j]
    p.stdin.write('reset; get hips(P/2MASS/color) '+obj+'; \n')
    # Zoom can be changed by the user.
    p.stdin.write('zoom 10arcmin; save '+name+'.jpg\n')
    j = j + 1

p.stdin.write('quit\n')
p.wait()
