import pyfpgrowth
import sys
from itertools import combinations 

args = sys.argv
min_sup = int(args[1])
filepath = args[2]
output = args[3]

t = open(filepath, "r+")

transactions = [he.split(",") for he in t.read().split("\n") if he.split(",") > 1]
print "Total transactions :", len(transactions)
patterns = pyfpgrowth.find_frequent_patterns(transactions, min_sup)

patterns_mapped_frequency = {} 
for key in patterns.keys():
	if len(key) > 1:
		patterns_mapped_frequency[",".join(sorted(key))] = patterns[key]

pat = [p.split(",") for p in patterns_mapped_frequency.keys()]
print "Frequent patterns with length > 2 :", len(pat)
maximum = max([len(p) for p in pat])
total_count = 0
for m in range(3,maximum+1)[::-1]:
	count_m = 0
	for p in patterns_mapped_frequency.keys():
		if len(p.split(",")) == m and patterns_mapped_frequency[p]>0:
			val = patterns_mapped_frequency[p]
			count_m += 1
			for k in range(2,m)[::-1]:
				comb = list(combinations(p.split(","),k))
				try:
					for cp in comb:
						patterns_mapped_frequency[",".join(sorted(cp))] -= val
				except:
					pass
	print "Frequent count of patterns of size " + str(m) + " :", count_m
	total_count += count_m

final_patterns = [p for p in patterns_mapped_frequency if patterns_mapped_frequency[p]>0]

print "Frequent count of patterns of size 2 :", len(final_patterns) - total_count
print "Frequent final patterns :", len(final_patterns)

g = open(output, "w+")
g.write("\n".join(final_patterns)) 
g.close()
