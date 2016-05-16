import sys
import re
from collections import Counter
import itertools

def extractData():
	data = open(sys.argv[1], 'r').readlines()
	out = open('out.seq', 'w')
	text = ''.join(data)
	regex = re.compile('ORIGIN(\s*([0-9][\satgc]*))*\/\/', re.MULTILINE)
	dna = re.compile('[atcg]+')
	seqId = 1
	
	for i in re.finditer(regex, text):
		sequence = ''
		for i in re.finditer(dna, i.group(0)):
			sequence += i.group(0)
		if len(sequence) >= 1000 and len(sequence) <= 1100:
			out.write('seqId ' + str(seqId) + '. length ' + str(len(sequence)) + '\n')
			out.write(sequence)
			out.write('\n')
			seqId += 1
	data.close()
	out.close()

def cutSequence(seq):
	cut = []
	for i in range(len(seq) - 9):
		cut.append(seq[i:i+10])
	cut.sort()
	return cut

def createEmptyMatrix():
	out = open('emptyMatrix.out', 'w')
	all = itertools.product('acgt', repeat=10)
	id = 0
	for i in all:
		if(id % 1024 == 0 and id != 0):
			out.write('\n')
		convert = ''.join(i)
		out.write(convert)
		out.write(', ')
		id += 1
	out.close()
	
def countSubsequences():
	seq = 'tttttttttttttttatttataacgcctattgtagattgataggctctaaatttacaaacctgaatcgtacagatttgtacgaccgtttgggaaaggtatgccattatcggatgtataaattaccaatgtatcatccttgaatcctgccttttctaattcttcaagaacaaggccaacgcctttatctaaacgagatattgttgtatattgggcagcaatatctcttcgagcagcttcggtattctgaacatagtatggtactttaacttgctcccattgataatatattggattccaatcgggaattgtacccattccaatatcaccattgccgaatttctcacaaaaattgccatactctggatgcgtatgcccacagcgatgcggatcgtgaaaggcaacatacagaaagaagggttgtgttttattttgtgaaagaaattcgcggacaagtagctttatataagtaatattgcgacctacttgaagaatagaattattttcttctgtatatgcaaaatcaaatggataaacattactgggacctacatgtttcttgccaataattcctgttcgtatattatttcttttcaatatttttggcaaacttttaatattatcaaaagaattaaaatgatgaactccttgatgaagaccatacatcccattttgatgacttggtaatccagttaatatcgtggagcggcttggtgaacagctactgactgatgtgtacgcattgttgaatagtagactttcctttgccaatttatccaaattaggagtttgacatatcttatttaagtacgatcgcatttcaaaacctgcatcatcagccagcaataggagcacattttttcgagatatatcggtttttccatttgtgcacaagacaatacacaaaagccataataatttattcaaacagctgttcaacgacatatcatacaattgtgaaacgtgcgtctgcgttagcggtatacgcgtgtaagcacgtgaccgtggctgcgttccgatatacactgca'
	matrix = Counter(cutSequence(seq))
	print(matrix)
