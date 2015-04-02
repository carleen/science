'''Reads in a csv file with given RA, DEC, and names of targets. Returns .jpg 
images of the finder chart for each given object in the csv file'''
import csv
import subprocess

#opens 
file = open('Boyer_targets_ordered.csv')
csv_file = csv.reader(file)

names = []
coordinates = []

i = 0
j = 0

for row in csv_file:
	if i != 0:
		names.append(row[0].replace(" ", ""))
		dec = row[2]
		dec = dec.replace("(", "") 
		dec = dec.replace(")", "")
		coordinates.append(row[1] + ' ' + dec)
	i = 1

p = subprocess.Popen(['java -jar /Applications/Aladin.app/Contents/Java/Aladin.jar'],
		shell=True,
		stdin=subprocess.PIPE
		)


p.stdin.write('grid on\n')
for obj in (coordinates):
	name = names[j]
	p.stdin.write('reset; get aladin '+name+'; get VizieR(GSC1.2); get simbad;\n')
	p.stdin.write('zoom 10arcmin; save '+name+'.jpg\n')
	j = j+1

p.stdin.write('quit\n')
p.wait()
