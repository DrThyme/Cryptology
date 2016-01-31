import string
import sys
import re
from collections import Counter
from bidict import bidict #Bidict might not work on the school computers.

codec = sys.stdin.encoding

# Dictionary containing all the allowed letters mapped to their number.
d = bidict({
	u'a': 0,
	u'b': 1,
	u'c': 2,
	u'd': 3,
	u'e': 4,
	u'f': 5,
	u'g': 6,
	u'h': 7,
	u'i': 8,
	u'j': 9,
	u'k': 10,
	u'l': 11,
	u'm': 12,
	u'n': 13,
	u'o': 14,
	u'p': 15,
	u'q': 16,
	u'r': 17,
	u's': 18,
	u't': 19,
	u'u': 20,
	u'v': 21,
	u'w': 22,
	u'x': 23,
	u'y': 24,
	u'z': 25,
	u'\xe5': 26,
	u'\xe4': 27,
	u'\xf6': 28,
	u' ': 29,
	u',': 30,
	u'.': 31
})

# A dictionary containing a frequency analysis of the Swedish language.
char_freq = {
	0: 0.072, 	#a
	1: 0.011, 	#b
	2: 0.013, 	#c
	3: 0.045, 	#d
	4: 0.084, 	#e
	5: 0.014, 	#f
	6: 0.032, 	#g
	7: 0.013, 	#h
	8: 0.044, 	#i
	9: 0.003, 	#j
	10: 0.025, 	#k
	11: 0.049, 	#l
	12: 0.027, 	#m
	13: 0.068, 	#n
	14: 0.036, 	#o
	15: 0.009, 	#p
	16: 0.0001, 	#q
	17: 0.080, 	#r
	18: 0.048, 	#s
	19: 0.072, 	#t
	20: 0.012, 	#u
	21: 0.021,	#v
	22: 0.0002,	#w	
	23: 0.003,	#x
	24: 0.004,	#y
	25: 0.0002,	#z
	26: 0.014,	#'a
	27: 0.019,	#''a
	28: 0.012,	#''o
	29: 0.151,	#(space)
	30: 0.008,	#,
	31: 0.011	#.
}

# This function is used to get all divisors for the provided number n.
# The divisors are returned as a list.
def getDivisors(n):
	l = []
	for i in range(2,n):
		if n % i == 0:
			l.append(i)
	return l

# This function is used to find the number of occurences for each substring
# with length <16 inside the string cipher. A sorted list of each substring
# and a count that substring is the returnedby the function.
def fileOcc(cipher):
	i=3
	l = []
	while i<16:
		j=0
		find = cipher[j:j+i]
		num = len(find)
		while num == i:
			occ = cipher.count(find)
			if occ > 1:
				if (find,occ) not in l:
					l.append((find,occ))
			j+=1
			find = cipher[j:j+i]
			num = len(find)
		i+=1
	ll = sorted(l,key=lambda x: len(x[0]), reverse=True)
	return ll

# This function finds the start index of every string find found in the
# string cipher.
# Ex: 	s = 'abcffffabcabc'
#	findLocation(s,'abc') => returns [0,7,10]
def findLocation(cipher, find):
	return [m.start() for m in re.finditer(find, cipher)]

# This function calculates the occurence of each character in the provided
# string text and returns the ratio of each character.
# This is used to make a frequency analysis of a text so that we can use it 
# for decoding the key.
def freqAnalysis(text):
	l = []
	char_list = list(text)
	occ = Counter(char_list)
	for i in range(0,32):
		ratio = occ[d.inv[i]]/float(len(text))
		l.append((d.inv[i],ratio))
	return l

# This functions cleans the provided string text of all characters that does
# not exist in our allowed alphabet.
# Ex:	cleanString(u'ab(32)CD') => returns u'abcd'
def cleanString(text):
	text = text.lower()
	text = text.rstrip('\n')
	allow=u'abcdefghijklmnopqrstuvwxyz\xe5\xe4\xf6 .,'
	convert = re.sub('[^%s]'%allow,'',text)
	return convert				 

# This function splits the provided string text length number of chunks
# each chunk will contain each character where i%mod length is the same.
# The function returns these chunks as a nested list.
# Ex:	splitString(3,'abcdef') => returns [['a','d'],['b','e'],['c','f']]
def splitString(length,text):
	l = []
	for i in range(0,length):
		l_new = [text[i+length*x] for x in range(0,len(text)/length)]
		l.append(l_new)
	return l	

####### This function is no longer in use #######
# This function takes a nested list, each list containing characters. 
# The function returns a list containing the most common character in each list.
# Ex:	findMostCommon([['a','a','b'],['a','c','d','d']] => returns ['a','b']
def findMostCommon(nl):
	common = []
	for l in nl:
		temp = Counter(l)
		common.append(temp.most_common()[0][0])
	return common

####### This function is no longer in use #######
# This function takes the given list of common characters and shifts them
# by 29 characters. This considers that space is the most common character in Swedish.
def shift(common):
	shift = []
	key = []
	for item in common:
		i = 29
		while (i%32) != d[item]:
			i+=1
		shift.append(d.inv[(i%29)])
	return shift

# This function takes a cipher and the number of substring occurences
# and returns a Counter of all possible divisors between the repeated
# occurences.
def getKeyLength(cipher,occ,limit):
	div = []
	first = True
	for t in occ:
		loc = findLocation(cipher,t[0])
		for i in range(0,len(loc)-1):
			divNum = getDivisors(loc[i+1]-loc[i])
			for num in divNum:
				if num <= limit:
					div.append(num)
	return Counter(div)

# Using the function in the slides (lecture 4) this function calculates the
# most probable key used to encrypt the cipher. This takes into count the 
# frequency analysis of the Swedish language.
def calcKey(split):
	l_temp = []
	l_k = []
	for item in split:
		occ = Counter(item)
		l_temp = []
		for k in range(0,32):
			sum = 0
			for i in range(0,32):
				num = occ[d.inv[(i+k)%32]]
				sum += (char_freq[i]*(num/float(len(item))))	
			l_temp.append(sum)
		best_k = max(l_temp)
		index_k = l_temp.index(best_k)
		l_k.append(d.inv[index_k])
	return l_k

# Main function for encrypting a file.
def encrypt(file,save,key):
	print '### Encrypting file %s, result will be saved in %s ###' % (file,save) 
	f = open(file,'r')
	plain = f.read()
	plain = plain.decode(codec)
	f.close()
	
	plain = cleanString(plain)

	key = key.decode(codec)
	i = 0
	cipher = u''

	for letter in plain:
        	key_letter = key[i%len(key)]
        	ciph_num = (d[letter]+d[key_letter])%32
        	cipher += d.inv[ciph_num]
        	i+=1

	f = open(save,'w')
	f.truncate()
	f.write(cipher.encode(codec))
	f.close()

# Main function for decrypting a file.
def decrypt(file,key):
	print '### Decoding ###' 
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	key = key.decode(codec)
	cipher = cleanString(cipher)

	i = 0
	decrypted = u''

	for letter in cipher:
        	key_letter = key[i%len(key)]
        	ciph_num = (d[letter]-d[key_letter])%32
        	decrypted += d.inv[ciph_num]
        	i+=1
	print decrypted
			
# Main function for calculating the key length of a file.
def keyLength(file):
	print '### Finding key length of supplied cipher ###' 
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	occ = fileOcc(cipher)	
	kl = getKeyLength(cipher,occ,16)
	print kl

# Main function for solving the most probable key to belonging to a cipher.
def crackKey(file,length):
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	nl = splitString(length,cipher)
	key = calcKey(nl)

	print 'The key might be: %s'%''.join(key)

# Dictionary for commands given to the script.
commands = {
	'encrypt' : encrypt,
	'decrypt' : decrypt,
	'keyLength' : keyLength,
	'crackKey' : crackKey
}

# Checks what command is given to the script and executes the corresponding function.
arg = sys.argv
if len(arg) == 3:
	commands[arg[1]](arg[2])
elif len(arg) == 4:
	if arg[1] == 'decrypt':
		commands[arg[1]](arg[2],arg[3])
	else:
		commands[arg[1]](arg[2],int(arg[3]))	
elif len(arg) == 5:
	commands[arg[1]](arg[2],arg[3],arg[4])
else:
	print 'Invalid amount of arguments'
