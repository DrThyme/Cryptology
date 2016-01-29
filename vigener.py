import string
import sys
import re
from collections import Counter
from bidict import bidict

codec = sys.stdin.encoding

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

def getDivisors(n):
	l = []
	for i in range(2,n):
		if n % i == 0:
			l.append(i)
	return l

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

def findLocation(cipher, find):
	return [m.start() for m in re.finditer(find, cipher)]

def freqAnalysis(text):
	l = []
	char_list = list(text)
	occ = Counter(char_list)
	for i in range(0,32):
		ratio = occ[d.inv[i]]/float(len(text))
		l.append((d.inv[i],ratio))
	return l

def cleanString(text):
	text = text.lower()
	text = text.rstrip('\n')
	allow=u'abcdefghijklmnopqrstuvwxyz\xe5\xe4\xf6 .,'
	convert = re.sub('[^%s]'%allow,'',text)
	return convert				 

def splitString(length,text):
	l = []
	for i in range(0,length):
		l_new = [text[i+length*x] for x in range(0,len(text)/length)]
		l.append(l_new)
	return l	

def findMostCommon(nl):
	common = []
	for l in nl:
		temp = Counter(l)
		common.append(temp.most_common()[0][0])
		#common.append(temp.most_common())	
	return common

def shift(common):
	shift = []
	key = []
	for item in common:
		i = 29
		while (i%32) != d[item]:
			i+=1
		shift.append(d.inv[(i%29)])
	return shift

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
			

def keyLength(file):
	print '### Finding key length of supplied cipher ###' 
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	occ = fileOcc(cipher)	
	kl = getKeyLength(cipher,occ,16)
	print kl

def crackKey(file,length):
	f = open(file,'r')
	cipher = f.read()
	cipher = cipher.decode(codec)
	f.close()

	nl = splitString(length,cipher)
	#common = findMostCommon(nl)
	key = calcKey(nl)

	print 'The key might be: %s'%''.join(key)

commands = {
	'encrypt' : encrypt,
	'decrypt' : decrypt,
	'keyLength' : keyLength,
	'crackKey' : crackKey
}

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

f = open('vig_group17.temp','r')
s = f.read()
f.close()
#print codec
s = s.decode(codec)
s = cleanString(s)
f = open('vig_group17.key','w')
f.write(s.encode(codec))
f.close()

#nl = splitString(5,s)
#anz = findMostCommon(nl)

#f = open('cipher.txt','r')
#c = f.read()
#f.close()
#c = c.decode(codec)
#c = cleanString(c)

#cl = splitString(11,c)
#cnz = findMostCommon(cl)
#keys = calcKey(cl)
#print keys
#print cnz

