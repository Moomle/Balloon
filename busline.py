#--*--coding=gb2312--*--
import sqlite3

def getConn():
	dbName = 'nanjing'#raw_input("DB Name:")
	try:
		conn = sqlite3.connect(dbName)
		return conn
	except:
		print 'db open error'
		return False

def closeConn(conn):
	try:
		conn.close()
	except:
		print 'error to close conn to db'

def chEncode(char):
	return char.decode('gb2312').encode('utf8')


def getLineZhanSet(conn, Zhan):
	xids = getLines(conn, Zhan)
	#put all the distinct stations into a list
	print 'len of xids is ', len(xids)
	stlist = []
	for xid in xids:	#get all the stations of every busline which got above 
		rsZhan = conn.execute("select distinct zhan from cnbus where xid == " + str(xid) + " and kind == 1 order by pm asc")
		zhan = rsZhan.fetchall()
		for z in zhan:
			stlist.append(z[0])
	nlist = []
	[nlist.append(x) for x in stlist if x not in nlist]
	#for i in nlist:
	#	print i.encode('gb2312'),
	#print ''
	#print 'stlist len is ', len(nlist)
	return nlist

def getRoute(srcSet, dstSet):
	routes = []
	[routes.append(x) for x in srcSet if x in dstSet]
	printList(routes)
	return routes

def getLines(conn, zhan):  #return lines across the zhan
	xids = []
	try:
		rsXid = conn.execute("select xid from cnbus where zhan == '" + zhan + "' and kind == 1 order by xid asc")
		xids = rsXid.fetchall()	#get the buslines cross the srcZhan
	except:
		print 'query error'
		return xids
	xids = [x[0] for x in xids]
	return xids

def printList(lst):
	for i in lst:
		if isinstance(i, str):
			print i.encode('gb2312'),

def getLineName(conn, xid):
	rs = conn.execute("select distinct busw from cnbusw where id == '" + str(xid) + "'")
	lst = rs.fetchall()
	lst = [x[0] for x in lst]
	return lst

conn = getConn()
srcLines = getLines(conn, chEncode('长途东站'))
dstLines = getLines(conn, chEncode('河海大学江宁校区'))
srcSet = getLineZhanSet(conn, chEncode('长途东站'))
dstSet = getLineZhanSet(conn, chEncode('河海大学江宁校区'))
crossZhans = getRoute(srcSet, dstSet)
tmpLines = getLines(conn, crossZhans[2])
midLine1 = getRoute(tmpLines, srcLines)
midLine2 = getRoute(tmpLines, dstLines)
s1=getLineName(conn, midLine1[0])
s2=getLineName(conn, midLine2[0])
print s1[0].encode('gb2312'), ' ', s2[0].encode('gb2312')