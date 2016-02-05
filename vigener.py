import string
import sys
import re
from collections import Counter
import timeit

#codec = sys.stdin.encoding
codec = 'utf-8'

# Dictionary containing all the allowed letters mapped to their number.
char_int = {
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
}

int_char = {
	0: u'a',
	1: u'b',
	2: u'c',
	3: u'd',
	4: u'e',
	5: u'f',
	6: u'g',
	7: u'h',
	8: u'i',
	9: u'j',
	10: u'k',
	11: u'l',
	12: u'm',
	13: u'n',
	14: u'o',
	15: u'p',
	16: u'q',
	17: u'r',
	18: u's',
	19: u't',
	20: u'u',
	21: u'v',
	22: u'w',
	23: u'x',
	24: u'y',
	25: u'z',
	26: u'\xe5',
	27: u'\xe4',
	28: u'\xf6',
	29: u' ',
	30: u',',
	31: u'.'
}

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
	print ll
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
		ratio = occ[int_char[i]]/float(len(text))
		l.append((int_char[i],ratio))
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
	print Counter(div)
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
				num = occ[int_char[(i+k)%32]]
				sum += (char_freq[i]*(num/float(len(item))))	
			l_temp.append(sum)
		best_k = max(l_temp)
		index_k = l_temp.index(best_k)
		l_k.append(int_char[index_k])
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
        	ciph_num = (char_int[letter]+char_int[key_letter])%32
        	cipher += int_char[ciph_num]
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
        	ciph_num = (char_int[letter]-char_int[key_letter])%32
        	decrypted += int_char[ciph_num]
        	i+=1
	print decrypted.encode(codec)
			
def keyLengthSpec(file):
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	occ = fileOcc(cipher)	
	kl = getKeyLength(cipher,occ,len(cipher))
	return list(kl)

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


def complete(file):
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	cipher = cleanString(cipher)
	
	sum=0
	ans = 'n'
	while ans=='n':	
		print '################################'
		print 'Possible key lengths displayed below:'
		start = timeit.default_timer()
		occ = fileOcc(cipher)	
		kl = getKeyLength(cipher,occ,16)
		stop = timeit.default_timer()
		print kl
		
		sum+=(stop-start)
	
		print '################################'
		inp = raw_input('Please enter key length: ')
		start = timeit.default_timer()
		nl = splitString(int(inp),cipher)
		key = calcKey(nl)
		stop = timeit.default_timer()
		sum+=(stop-start)
	
		print '################################'
		print 'The key might be: %s'%''.join(key)
		print '################################'
		
		print 'Now decoding file using key: '+''.join(key)

		i = 0
		decrypted = u''

		key = ''.join(key)
		start = timeit.default_timer()
		for letter in cipher:
        		key_letter = key[i%len(key)]
        		ciph_num = (char_int[letter]-char_int[key_letter])%32
        		decrypted += int_char[ciph_num]
        		i+=1
		stop = timeit.default_timer()
		sum+=(stop-start)
		print decrypted
		ans = raw_input('Does this look right? (y/n/k): ')
		if ans == 'k':
			key = raw_input('Use what key? ')
			key = key.decode(codec)
			decrypted  = ''
			i = 0
			print 'Now decoding file using key: '+key
			for letter in cipher:
        			key_letter = key[i%len(key)]
        			ciph_num = (char_int[letter]-char_int[key_letter])%32
        			decrypted += int_char[ciph_num]
        			i+=1
			print decrypted
			ans = raw_input('Does this look right? (y/n): ')
			
	print decrypted.encode(codec)

	## The following part can be used for saving the result to a file	
	#f = open('result.txt','a')
	#f.write(file)
	#f.write('\n')
	#f.write('The key was: %s \n'%key.encode(codec))
	#f.write(decrypted.encode(codec))
	#f.write('\n## Runtime: %s'%str(sum))
	#f.write('\n\n')
	#f.close()
	print 'DONE'
	#print decrypted

# Used for decrypting ciphers with long key.
def special():
	t1 = load('ciphers/text1.crypto')
	t2 = load('ciphers/text2.crypto')
	t3 = load('ciphers/text3.crypto')
	t4 = load('ciphers/text4.crypto')
	t5 = load('ciphers/text5.crypto')

	a = keyLengthSpec('ciphers/text1.crypto')
	b = keyLengthSpec('ciphers/text2.crypto')
	c = keyLengthSpec('ciphers/text3.crypto')
	d = keyLengthSpec('ciphers/text4.crypto')
	e = keyLengthSpec('ciphers/text5.crypto')

	l = [t1,t2,t3,t4,t5]
	res = set(a) & set(b) & set(c) & set(e) #& set(d)   ## Omit text4 since it doesn't have 214 as divisor
	print res
	kl = raw_input('Enter key length: ')
	kl = int(kl)
	total = u''
	for item in l:
		end = len(item)-len(item)%kl
		total = total + item[:end]
	nl = splitString(kl,total)
	key = calcKey(nl)

	print u''.join(key)
	
def load(file):
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	cipher = cleanString(cipher)
	return cipher
	
	
# Dictionary for commands given to the script.
commands = {
	'encrypt' : encrypt,
	'decrypt' : decrypt,
	'keyLength' : keyLength,
	'crackKey' : crackKey,
	'complete' : complete,
	'special' : special
}

# Checks what command is given to the script and executes the corresponding function.
arg = sys.argv
if len(arg) == 2:
	commands[arg[1]]()
elif len(arg) == 3:
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

