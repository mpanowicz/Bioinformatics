import sys
import re
from collections import Counter, OrderedDict
import itertools

toFile = False		#Choose if create emptyMatrix file
log = False		#Display additional info to console
consoleLog = True	#Log all data froim console to file
clearConsoleLog = True	#Create new console.log file
menu = 'Options:\n1) extractData - Create file with sequences based on file downloaded from DNA bank, parameters: file path to *.seq creates file out.seq\n2) getSequence - Retrive choosen sequence from created file, parameters: file path to out.seq, sequence id\n3) countSubsequences - Count amount of subsequences, parameters: file path to out.seq, sequence id\n4) matrixBasedOnSequence - Create full matrix without mistakes, parameters: file path to out.seq, sequence id'

def logging():
	if consoleLog :
		if clearConsoleLog : 
			open('console.log', 'w')
		sys.stdout = open('console.log', 'a')

def switch():
	if len(sys.argv) > 1 :
		if sys.argv[1] == 'extractData':
			logging()
			extractData(sys.argv[2])
		elif sys.argv[1] == 'getSequence':
			logging()
			getSequence(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == 'countSubsequences':
			logging()
			countSubsequences(getSequence(sys.argv[2], sys.argv[3]))
		elif sys.argv[1] == 'matrixBasedOnSequence':
			logging()
			matrixBasedOnSequence(countSubsequences(getSequence(sys.argv[2], sys.argv[3])))
		else : print('Choose other option\n' + menu)
	else: print(menu)

def extractData(file):
	if log == True : print('Read input file')
	data = open(file, 'r').readlines()
	out = open('out.seq', 'w')
	text = ''.join(data)
	regexText = 'ORIGIN(\s*([0-9][\satgc]*))*\/\/'
	regex = re.compile(regexText, re.MULTILINE)
	dnaText = '[atcg]+'
	dna = re.compile(dnaText)
	seqId = 1
	if log == True : print('Extract data based on regex ' + regexText)
	for i in re.finditer(regex, text):
		sequence = ''
		if log == True : print('Extract data based on regex ' + dnaText)
		for j in re.finditer(dna, i.group(0)):
			sequence += j.group(0)
		if log == True : print('If sequence length between 1000 and 1100 add it to file out.seq')
		if len(sequence) >= 1000 and len(sequence) <= 1100:
			out.write('seqId ' + str(seqId) + '. length ' + str(len(sequence)) + '\n')
			out.write(sequence)
			out.write('\n')
			seqId += 1
	out.close()

def cutSequence(seq):
	if log == True : print('Cut given sequence into 10 letter length subsequences')
	cut = []
	for i in range(len(seq) - 9):
		cut.append(seq[i:i+10])
	if log == True : print('cutSequence: ', cut)
	return cut

def createEmptyMatrix():
	if toFile :
		out = open('emptyMatrix.out', 'w')
	matrix = []
	if log == True : print('Create all Variations with repetition for acgt and 10 letter length')
	all = itertools.product('acgt', repeat=10)
	id = 0
	row = []
	if log == True : print('Format (\'a\', \'c\', ...) objects into ac.. strings')
	if log == True : print('Create matrix with elements {\'acgtactgaa\' : 0}')
	for i in all:
		if(id % 1024 == 0 and id != 0):
			if toFile :
				out.write('\n')
			matrix.append(row)
			row = []
		convert = ''.join(i)
		row.append({convert: 0})
		if toFile :
			out.write(convert)
			out.write(', ')
		id += 1
	matrix.append(row)
	if toFile :
		out.close()
	array = {}
	for i in matrix:
		for j in i:
			for sub in j: 
				array[sub] = j[sub]
	return array

def getSequence(file, number):
	if log == True : print('Retrive choosen sequence')
	text = ''.join(open(file, 'r').readlines())
	regexNumber = 'seqId ' + number + '. length \d{4}\n[acgt]+'
	regex = re.compile(regexNumber, re.MULTILINE)
	id = re.findall(regex, text)[0]
	regexSequence = '[acgt]+'
	regex = re.compile(regexSequence)
	if log == True : print('getSequence: ', [id, re.findall(regex, id)[1]])
	return [id, re.findall(regex, id)[1]]

def countSubsequences(seq):
	cutted = cutSequence(seq[1])
	if log == True : print('Count subsequences in given sequence')
	subsequencesDict = dict(Counter(cutted))
	orderedDict = OrderedDict(sorted(subsequencesDict.items()))
	array = {}
	for sub, count in orderedDict.items():
		array[sub] = count
	if log == True : print('countSubsequences: ', array)
	return(array)

def matrixBasedOnSequence(count):
	empty = createEmptyMatrix()
	for i in count:
		empty[i] = count[i]
	matrix = sorted(empty.items())
	if log == True : print('matrixBasedOnSequence: ', matrix)
	return matrix

switch()