import requests
requests.packages.urllib3.disable_warnings()
import cobra.mit.access
import cobra.mit.access as mo
import cobra.mit.session as session
import cobra.mit.request
import cobra.mit.session
from tabulate import tabulate
import time
import requests.packages.urllib3
import datetime

def main():
	mo = cobra.mit.access
	apicurl = 'http://10.124.4.101'
	mo_dir = mo.MoDirectory(session.LoginSession(apicurl, 'admin', 'Cisco123'))
	mo_dir.login()
	topology(mo_dir)
	for i in range(1,30):
		if i<=30:
			time.sleep(2)
		y = i+1
		table(i,mo_dir)

def topology(mo):
	topology = cobra.mit.access.ClassQuery('fabricTrail')
	fabricTrail_objlist = mo.query(topology)
	dbgAclist_0 = []
	for n in fabricTrail_objlist:
		row_1 = [
			n.rn,
			n.transit,
			n.n1,
			n.n2,
		]
		dbgAclist_0.append(row_1)
	print tabulate(sorted(dbgAclist_0), tablefmt='grid', headers=["Trail", "Transit", "Nold_1", "Nold_2"])

def table(i,mo):
	clAcPath = cobra.mit.access.ClassQuery('dbgAcPath')
	dbgAcPathA_objlist = mo.query(clAcPath)
	dbgAclist = []
	now = datetime.datetime.now()

	for m in dbgAcPathA_objlist:
		# if int(m.dropPkt) != 0:
		row_2 = [
			m.rn,
			m.txPkt,
			m.rxPkt,
			m.dropPkt,
			m.totDropPkt,
			m.totDropPktPercentage,
			now.strftime('%Y-%m-%d %H:%M:%S'),
		]
		dbgAclist.append(row_2)

	print tabulate(dbgAclist,tablefmt='simple',headers=["Path","TransceivePakets","ReceivePakets","DropPackets","TotalDropPackets","TotalDropPacketsPercentage","Time"])
	return

if __name__ == '__main__':
	main()