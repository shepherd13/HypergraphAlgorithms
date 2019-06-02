from collections import defaultdict, OrderedDict, Counter
from datetime import datetime, timedelta
import json

fname = 'loc-gowalla_totalCheckins.txt'
#fname = "test.txt"
e = open('outputs/error.txt', 'w+')

def mapID(sequence, start):
	dictionary = dict(enumerate(sequence, start))
	reverse_dictionary = dict((v, k) for k, v in dictionary.iteritems())
	return reverse_dictionary

locations = set()
users = set()
transaction_dict = defaultdict()

with open(fname) as f:
	for line in f:
		try:
			lst = line.split('\t')
			uid, ts, lat, lon, vid = map(lambda x: x.strip(), lst)
			users.add(uid)
			time = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')
			day = time.strftime('%Y-%m-%d')
			if vid not in locations:
				transaction_dict[vid] = dict()
			if (day,time.hour) not in transaction_dict[vid].keys():
				transaction_dict[vid][(day,time.hour)] = set()
			transaction_dict[vid][(day,time.hour)].add(uid)
			locations.add(vid)
		except:
			e.write(line+"\n")
			continue	

orderedTransaction_dict = defaultdict(OrderedDict)
for loc in transaction_dict.keys():
	td_keys = transaction_dict[loc].keys()
	sdt = sorted([datetime.strptime(dt[0]+'T'+str(dt[1]), '%Y-%m-%dT%H') for dt in td_keys])
	for dt in sdt:
		orderedTransaction_dict[loc][(dt.strftime('%Y-%m-%d'), dt.hour)] = transaction_dict[loc][(dt.strftime('%Y-%m-%d'), dt.hour)]

orderedTransaction_dict2 = defaultdict(OrderedDict)
for loc in orderedTransaction_dict.keys():
	td_keys = orderedTransaction_dict[loc].keys()
	for tdk in td_keys:
		orderedTransaction_dict2[loc][tdk[0]+", "+str(tdk[1])] = ",".join(orderedTransaction_dict[loc][(tdk[0], tdk[1])])

with open("outputs/orderedTransaction.json", 'w+') as o:
	json.dump(orderedTransaction_dict2, o)

#user_dict = mapID(users, 1)
authors_set = set()
authors_group_list = list()
group_time_loc_list = list()

hour_range = 1
for loc in orderedTransaction_dict.keys():
	td_keys = orderedTransaction_dict[loc].keys()
	for dth_index in range(len(td_keys)):
		group = orderedTransaction_dict[loc][td_keys[dth_index]]
		g_time = td_keys[dth_index]
		for hr in range(1,hour_range+1):
			if dth_index+hr in range(len(td_keys)):
				if td_keys[dth_index+hr][0] == td_keys[dth_index][0] and td_keys[dth_index+hr][1] <= td_keys[dth_index][1]+hour_range:
					group = group|orderedTransaction_dict[loc][td_keys[dth_index+hr]]
				elif td_keys[dth_index+hr][0] == (datetime.strptime(td_keys[dth_index][0], '%Y-%m-%d')+timedelta(days=1)).strftime('%Y-%m-%d') and td_keys[dth_index+hr][1] <= (td_keys[dth_index][1]+hour_range)%24:
					group = group|orderedTransaction_dict[loc][td_keys[dth_index+hr]]
			if dth_index-hr in range(len(td_keys)):
				if td_keys[dth_index-hr][0] == td_keys[dth_index][0] and td_keys[dth_index-hr][1] >= td_keys[dth_index][1]-hour_range:
					group = group|orderedTransaction_dict[loc][td_keys[dth_index-hr]]
				elif td_keys[dth_index-hr][0] == (datetime.strptime(td_keys[dth_index][0], '%Y-%m-%d')-timedelta(days=1)).strftime('%Y-%m-%d') and (td_keys[dth_index-hr][1]+hour_range)%24 >= td_keys[dth_index][1]:
					group = group|orderedTransaction_dict[loc][td_keys[dth_index-hr]]

		authors_set.update(group)
		authors_group_list.append(",".join(sorted(group)))
		group_time_loc_list.append([",".join(sorted(group)), g_time[0], g_time[1], loc])

authors_mappedID = mapID(authors_set, 1)
# with open("output_filter/authors_mappedID.json", 'w+') as q:
# 	json.dump(authors_mappedID, q)

with open('outputs/timed_transactions.csv', 'w+') as h:
	for gtl in group_time_loc_list:
		group = gtl[0]
		if len(group.split(",")) > 1:
			g = map(lambda author: str(authors_mappedID[author]), group.split(","))
			h.write(",".join(g)+"\t"+gtl[1]+"\t"+str(gtl[2])+"\t"+gtl[3]+'\n')

with open('outputs/transactions.csv', 'w+') as h:
	for group in authors_group_list:
		if len(group.split(",")) > 1:
			g = map(lambda author: str(authors_mappedID[author]), group.split(","))
			h.write(",".join(g)+'\n')
