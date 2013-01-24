"""
Title: Descriptives
Description: Computes descriptive statistics from a .csv dataset
Usage:
Date Started: 2013 Jan
http://www.asymptoticdesign.org/

Description of Usage:
scottnla@faraday-cage:~/$ python readSerial.py [filename]
Reads serial information from an arduino circuit, writes it to file.
"""

import sys
import csv
import scipy
import pylab
import csv
import kanonlib

def flattenToList(input):
	output = list(reduce(lambda p,q: p+q, input))
	return output

def writeToFile(list,filename):
	outputfile = open(filename+'.csv','w')
	for pair in list:
		outputfile.write(",".join([str(float(item)) for item in pair]) + "\n")
	outputfile.close()

#add writetofile
def agg_stats(fieldName):
	minQuery = "SELECT MIN(" + fieldName + ") FROM trips"
	min = hubway.MySQLquery(minQuery)[0][0]
	print "Field Mininum:",min
	maxQuery = "SELECT MAX(" + fieldName + ") FROM trips"
	max = hubway.MySQLquery(maxQuery)[0][0]
	print "Field Maximum:",max
	avgQuery = "SELECT AVG(" + fieldName + ") FROM trips"
	avg = hubway.MySQLquery(avgQuery)[0][0]
	print "Field Mean:",avg
	stdQuery = "SELECT STDDEV_SAMP(" + fieldName + ") FROM trips"
	std = hubway.MySQLquery(stdQuery)[0][0]
	print "Field Std:",std
	return [min,max,avg,std]

def dateQuery(dateField,filename="output"):
	queryString = "SELECT HOUR(%s), COUNT(*) AS frequency FROM trips GROUP BY HOUR(%s) ORDER BY %s;" %(dateField, dateField, dateField)
	freq = hubway.MySQLquery(queryString)
#	writeToFile(freq,filename)
	return freq[1:]

def stationQuery(stationField,filename="output"):
	queryString = "SELECT %s, COUNT(*) AS frequency FROM stations GROUP BY %s ORDER BY %s;" %(stationField,stationField,stationField)
	freq = hubway.MySQLquery(queryString)
#       	writeToFile(freq[1:],filename)
	return freq[1:]

def modal_stats(fieldName,filename="output"):
	freqQuery = "SELECT %s, COUNT(%s) AS frequency FROM trips GROUP BY %s ORDER BY %s;" %(fieldName,fieldName,fieldName,fieldName)
	freqs = hubway.MySQLquery(freqQuery)
#	print "Mode:",freqs[0]
	print "Unique Items:",len(freqs)
	#write to file here
	writeToFile(freqs[1:],filename)
	return freqs[1:]

def plotData(frequencies,abscissa='Absicca [units]',ordinate='No. [counts]',title='Hubway DataViz'):
	bins = []
	counts = []
	for pair in frequencies:
		bins.append(pair[0])
		counts.append(pair[1])

	pylab.bar(bins,counts)
	pylab.xlabel(abscissa,{'fontsize':20})
	pylab.ylabel(ordinate,{'fontsize':20})
	pylab.title(title,{'fontsize':20})
	pylab.grid()
	pylab.show()

def plotMonths(frequencies,abscissa='Absicca [units]',ordinate='No. [counts]',title='Hubway DataViz'):

	bins2011 = []
	counts2011 = []
	bins2012 = []
	counts2012 = []
	for triplet in frequencies:
		if triplet[0] == 2011:
			bins2011.append(triplet[1])
			counts2011.append(triplet[2])
		if triplet[0] == 2012:
			bins2012.append(triplet[1])
			counts2012.append(triplet[2])

	maxY = max(max(counts2012),max(counts2011))

	pylab.bar(bins2012,counts2012,label='2012',color='b')
	pylab.bar(bins2011,counts2011,label='2011',color='r')
	pylab.xlabel(abscissa,{'fontsize':20})
	pylab.ylabel(ordinate,{'fontsize':20})
	pylab.title(title,{'fontsize':20})
	pylab.grid()
	pylab.xlim(1,13)
	pylab.ylim(0,maxY+0.1*maxY)
	pylab.legend(loc=0)


	pylab.show()

def plotStations(freqIn,freqOut,abscissa='Absicca [units]',ordinate='No. [counts]',title='Hubway DataViz'):

	binsIn = []
	countsIn = []
	binsOut = []
	countsOut = []
	for pair in freqIn:
		print pair
		binsIn.append(pair[0])
		countsIn.append(pair[1])
	for pair in freqOut:
		binsOut.append(pair[0])
		countsOut.append(-1*pair[1])

	maxY = max(max(countsIn),abs(min(countsOut)))

	pylab.bar(binsIn,countsIn,label='In',color='b')
	pylab.bar(binsOut,countsOut,label='Out',color='r')
	pylab.xlabel(abscissa,{'fontsize':20})
	pylab.ylabel(ordinate,{'fontsize':20})
	pylab.title(title,{'fontsize':20})
	pylab.grid()
	pylab.legend(loc=0)
	pylab.ylim(-1.1*maxY,1.1*maxY)

	pylab.show()

def plotStationDiff(freqIn,freqOut,abscissa='Absicca [units]',ordinate='No. [counts]',title='Hubway DataViz'):

	bins = []
	counts = []
	for i in range(len(freqIn)):
		bins.append(freqIn[i])
		counts.append(freqIn[i] - freqOut[i])

	maxY = max(counts)

	pylab.bar(bins,counts)
	pylab.xlabel(abscissa,{'fontsize':20})
	pylab.ylabel(ordinate,{'fontsize':20})
	pylab.title(title,{'fontsize':20})
	pylab.grid()
	pylab.ylim(-1.1*maxY,1.1*maxY)

	pylab.show()

def countIdentifiers():
	response = kanonlib.MySQLquery("SELECT Zipcode, Birthdate, Gender, COUNT(*) FROM CambridgeVotingRecord GROUP BY Zipcode, Birthdate, Gender;")
	return response

def deanonymize():
    response = kanonlib.MySQLquery("SELECT hubway.trips.id, VotingRecords.CambridgeVotingRecord.First_Name, VotingRecords.CambridgeVotingRecord.Last_Name FROM hubway.trips, VotingRecords.CambridgeVotingRecord WHERE hubway.trips.zip_code = VotingRecords.CambridgeVotingRecord = Zipcode;")
    for row in response:
        print row

deanonymize()



#output = open("votingrecord_output.dat",'w')

#resp = countIdentifiers()

#for row in resp:
#	if row[1].year > 1900:
        #		output.write(row[0] + ",")
		#output.write(row[1].strftime("%y/%m/%d") + ",")
		#output.write(row[2] + ",")
		#output.write(str(int(row[3])) + "\n")

        #output.close()
