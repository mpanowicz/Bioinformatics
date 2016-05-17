import sys
import re
from collections import Counter, OrderedDict
import itertools

toFile = False		#Choose if create emptyMatrix file
log = True		#Display additional info to console
consoleLog = True	#Log all data froim console to file
clearConsoleLog = True	#Create new console.log file

if consoleLog :
	if clearConsoleLog : open('console.log', 'w')
	sys.stdout = open('console.log', 'a')

def extractData():
	if log : print('Read input file')
	data = open(sys.argv[1], 'r').readlines()
	out = open('out.seq', 'w')
	text = ''.join(data)
	regexText = 'ORIGIN(\s*([0-9][\satgc]*))*\/\/'
	regex = re.compile('ORIGIN(\s*([0-9][\satgc]*))*\/\/', re.MULTILINE)
	dnaText = '[atcg]+'
	dna = re.compile('[atcg]+')
	seqId = 1
	if log : print('Extract data based on regex ' + regexText)
	for i in re.finditer(regex, text):
		sequence = ''
		if log : print('Extract data based on regex ' + dnaText)
		for i in re.finditer(dna, i.group(0)):
			sequence += i.group(0)
		if log : print('If sequence length between 1000 and 1100 add it to file out.seq')
		if len(sequence) >= 1000 and len(sequence) <= 1100:
			out.write('seqId ' + str(seqId) + '. length ' + str(len(sequence)) + '\n')
			out.write(sequence)
			out.write('\n')
			seqId += 1
	out.close()

def cutSequence(seq):
	if log : print('Cut given sequence into 10 letter length subsequences')
	cut = []
	for i in range(len(seq) - 9):
		cut.append(seq[i:i+10])
	cut.sort()
	return cut

def createEmptyMatrix():
	if toFile :
		out = open('emptyMatrix.out', 'w')
	matrix = []
	if log : print('Create all Variations with repetition for acgt and 10 letter length')
	all = itertools.product('acgt', repeat=10)
	id = 0
	row = []
	if log : print('Format (\'a\', \'c\', ...) objects into ac.. strings')
	if log : print('Create matrix with elements {\'acgtactgaa\' : 0}')
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
	if toFile :
		out.close()
	return matrix
	
def countSubsequences():
	seq = 'tttttttttttttttatttataacgcctattgtagattgataggctctaaatttacaaacctgaatcgtacagatttgtacgaccgtttgggaaaggtatgccattatcggatgtataaattaccaatgtatcatccttgaatcctgccttttctaattcttcaagaacaaggccaacgcctttatctaaacgagatattgttgtatattgggcagcaatatctcttcgagcagcttcggtattctgaacatagtatggtactttaacttgctcccattgataatatattggattccaatcgggaattgtacccattccaatatcaccattgccgaatttctcacaaaaattgccatactctggatgcgtatgcccacagcgatgcggatcgtgaaaggcaacatacagaaagaagggttgtgttttattttgtgaaagaaattcgcggacaagtagctttatataagtaatattgcgacctacttgaagaatagaattattttcttctgtatatgcaaaatcaaatggataaacattactgggacctacatgtttcttgccaataattcctgttcgtatattatttcttttcaatatttttggcaaacttttaatattatcaaaagaattaaaatgatgaactccttgatgaagaccatacatcccattttgatgacttggtaatccagttaatatcgtggagcggcttggtgaacagctactgactgatgtgtacgcattgttgaatagtagactttcctttgccaatttatccaaattaggagtttgacatatcttatttaagtacgatcgcatttcaaaacctgcatcatcagccagcaataggagcacattttttcgagatatatcggtttttccatttgtgcacaagacaatacacaaaagccataataatttattcaaacagctgttcaacgacatatcatacaattgtgaaacgtgcgtctgcgttagcggtatacgcgtgtaagcacgtgaccgtggctgcgttccgatatacactgca'
	cutted = cutSequence(seq)
	if log : print('Count subsequences in given sequence')
	subsequencesDict = dict(Counter(cutted))
	orderedDict = OrderedDict(sorted(subsequencesDict.items()))
	return orderedDict

countSubsequences()

