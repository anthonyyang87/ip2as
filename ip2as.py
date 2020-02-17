import sys
import os


#read in from using readline and put in list
#read in from data base and sot

#for loop

def ReadAndParseFile(a, b): 
	try:
		temp1 = open(a)
	except Exception as e:
		raise "File not found"
	#read in IPlist
	try:
		temp2 = open(b)
	except Exception as e:
		raise "File not found"

	DBlist = []
	Dblines = temp1.read().splitlines()
	for i in range(len(Dblines) - 1):
		temp3 = Dblines[i].split()
		DBlist.append(temp3)

	IPlist = temp2.read().splitlines()

	return DBlist, IPlist

def BitWise(ipaddr):
	ipaddr = ipaddr.split('.')
	for i in range(len(ipaddr)):
		ipaddr[i] = format(int(ipaddr[i]), '08b')

	newIpaddr = ipaddr[0] + '.' + ipaddr[1] + '.' + ipaddr[2] + '.' + ipaddr[3]

	return newIpaddr

def GetPrefix(ipaddr, mask):
	ipaddr = BitWise(ipaddr).replace('.', '')
	prefix = ipaddr[:mask]
	return prefix

#this is not used in this program
def CreatePrefixDictionary(DBlist):
	dict = {}
	for i in range(len(DBlist)):
		try: 
			prefix = GetPrefix(DBlist[i][0], int(DBlist[i][1])) 
			dict[prefix] = DBlist[i][2]
		except:
			pass

def MatchLongestPrefixAndPrint(DBlist, IPlist):
	tempStore = {}
	tempStore2 = {}
	for ip in IPlist: #iterating through list of ips
		for i in range(len(DBlist)): #iterating through db
			try:
				#getting targeted prefix for matching purpose
				prefix1 = GetPrefix(DBlist[i][0], int(DBlist[i][1]))
				prefix2 = GetPrefix(ip, int(DBlist[i][1]))

				#store if the prefix of targeted ip and ip from db match
				if prefix1 == prefix2:
					#using dictionary here
					tempStore[DBlist[i][0]] = int(DBlist[i][1]) 
					tempStore2[DBlist[i][0]] = DBlist[i][2]
			except:
				pass

		#finding optimal match by comparing mask length
		optimalDomain = max(tempStore, key=tempStore.get)
		AS = tempStore2[optimalDomain]
		print optimalDomain + '/' + str(tempStore[max(tempStore)]) + ' ' + \
						AS + ' ' + ip
		#clearing temporary storage
		tempStore.clear()
		tempStore2.clear()

def main():
	#read in database file 
	DBlist, IPlist = ReadAndParseFile(sys.argv[1], sys.argv[2])
	MatchLongestPrefixAndPrint(DBlist, IPlist)
	
if __name__ == '__main__':
	main()
