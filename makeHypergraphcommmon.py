 # -*- coding: utf-8 -*-

from collections import defaultdict
import sys
from datetime import datetime
import unicodedata
import ast
import os
import shutil
from CreateHypergraph import CategoryBasedHypergraph, SimpleHypergraph

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = u'█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

def remove_accents(input_str):
	encoding = 'utf-8'
	input_str = input_str.decode('unicode_escape').encode(encoding).decode(encoding)
	nfkd_form = unicodedata.normalize('NFKD', input_str)
	only_ascii = nfkd_form.encode('ASCII', 'ignore')
	return only_ascii

def dblp():
	# These three dictionaries are required by the CategoryBasedHypergraph class
	cat_mapped_authors = defaultdict(set)
	cat_mapped_groups = defaultdict(set)
	group_mapped_time = defaultdict(set)

	categories_mapped_journal = defaultdict(list)
	for cat in os.listdir(support):
		journals = open(support+"/"+cat, "r+").read().lower().split('\n')
		journals = filter(lambda j: j!='', journals)
		categories_mapped_journal[cat[:-4]] = journals

	data_files = os.listdir(dataset)
	count = 0
	end = len(data_files)
	printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
	for file in range(end):
		for line in open(dataset+"/"+data_files[file], "r+"):
			try:
				dt = ast.literal_eval(line)['year']
				if dt >= start_year and dt <= end_year:
					time = datetime.strptime(str(dt), '%Y').strftime('%Y%m%d')
					venue = ast.literal_eval(line)['venue'].lower()
					for cat in categories_mapped_journal:
						if venue in categories_mapped_journal[cat]:
							authors = ast.literal_eval(line)['authors']
							group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','')) for author in authors])).strip(",| ")
							
							group_mapped_time[group].add(time)
							cat_mapped_groups[cat].add(group)
							cat_mapped_authors[cat].update([author for author in group.split(",") if author != ''])
			except:
				error.write(line+'\n')
		count += 1
		printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

	dblp = CategoryBasedHypergraph(group_mapped_time, cat_mapped_authors, cat_mapped_groups, output)
	dblp.generate_complete_hypergraph()
	dblp.generate_category_based_hypergraph()

def dblp_complete():
	# These three dictionaries are required by the SimpleHypergraph class
	authors_set = set()
	group_mapped_time = defaultdict(set)

	data_files = os.listdir(dataset)
	count = 0
	end = len(data_files)
	printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
	for file in range(end):
		for line in open(dataset+"/"+data_files[file], "r+"):
			try:
				dt = ast.literal_eval(line)['year']
				if dt >= start_year and dt <= end_year:
					time = datetime.strptime(str(dt), '%Y').strftime('%Y%m%d')
					authors = ast.literal_eval(line)['authors']
					group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','')) for author in authors])).strip(",| ")

					group_mapped_time[group].add(time)
					authors_set.update(group.split(","))
			except:
				error.write(line+'\n')
		count += 1
		printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

	dblp = SimpleHypergraph(group_mapped_time, authors_set, output)
	dblp.generate_complete_hypergraph()

def pubmed():
	cat_mapped_authors = defaultdict(set)
	cat_mapped_groups = defaultdict(set)
	group_mapped_time = defaultdict(set)

	categories_mapped_journal = defaultdict(list)
	for cat in os.listdir(support):
		journals = open(support+"/"+cat, "r+").read().lower().split('\n')
		journals = filter(lambda j: j!='', journals)
		categories_mapped_journal[cat[:-4]] = journals

	print categories_mapped_journal

	count = 0
	end = end_year-start_year + 1
	printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
	for year in range(start_year, end_year+1):
		for line in open(dataset+"/pubmed_"+str(year)+".txt"):
			a = line.strip().split('\t')
			if a[7] != '':
				try:
					time = datetime.strptime(a[1].strip(), '%Y/%m/%d %H:%M')
					venue = a[13].lower()
					print venue
					for cat in categories_mapped_journal:
						if venue in categories_mapped_journal[cat]:
							print venue
							group = ",".join(sorted([remove_accents(author) for author in a[7].strip(",| ").split(",")]))
							print group
							group_mapped_time[group].add(time)
							cat_mapped_groups[cat].add(group)
							cat_mapped_authors[cat].update([author for author in group.split(",") if author != ''])
				except:
					error.write(line+'\n')
		count += 1
		printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

	pubmed = CategoryBasedHypergraph(group_mapped_time, cat_mapped_authors, cat_mapped_groups, output)
	pubmed.generate_complete_hypergraph()
	pubmed.generate_category_based_hypergraph()


if __name__ == '__main__':

	args = sys.argv
	output_type = args[1]
	dataset = args[2]
	start_year = int(args[3])
	end_year = int(args[4])
	output = args[5]
	if output_type == "category":
		support = args[6]
	
	# Check if output folder exists
	output += "_"+str(start_year)+"_"+str(end_year)
	if not os.path.exists(output):
		os.makedirs(output)
	else:
		shutil.rmtree(output)
		os.makedirs(output)

	error = open(output+"/error.txt", "w")
	#dblp()
	pubmed()
	error.close()

"""
# Map all co-author groups to ID's
groups_mapped_ID = defaultdict()
groups_mapped_ID = mapID(group_mapped_time.keys(), 1)

# Map all authors to ID's
authors_mapped_ID = defaultdict()
authors_set = reduce(lambda a,s: a|s, cat_mapped_authors.values(),set())
authors_mapped_ID = mapID(authors_set, 1)

# Map category based authors to ID
cat_mapped_authors_mapped_authors_catID = defaultdict(dict)
cat_mapped_authors_catID_mapped_authors_ID = defaultdict(dict)
for cat, authors in cat_mapped_authors.iteritems():
	cat_mapped_authors_mapped_authors_catID[cat] = mapID(authors, 1)
	for author, author_catID in cat_mapped_authors_mapped_authors_catID[cat].iteritems():
		cat_mapped_authors_catID_mapped_authors_ID[cat][author_catID] = authors_mapped_ID[author]
	logs.write("Training authors for category " + str(cat) + " : " +str(len(cat_mapped_authors[cat])) + "\n")

# Map category based co-author groups to ID
cat_mapped_group_mapped_group_catID = defaultdict(dict)
cat_mapped_group_catID_mapped_group_ID = defaultdict(dict)
for cat, groups in cat_mapped_groups.iteritems():
	cat_mapped_group_mapped_group_catID[cat] = mapID(groups, 1)
	for group, group_catID in cat_mapped_group_mapped_group_catID[cat].iteritems():
		cat_mapped_group_catID_mapped_group_ID[cat][group_catID] = groups_mapped_ID[group]
	logs.write("Training Hyperedges for category " + str(cat) + " : " + str(len(cat_mapped_groups[cat])) + "\n")

# Map category based hyperedge ID to time and hyperedge ID to authors ID
cat_mapped_group_ID_mapped_time = defaultdict(list)
cat_mapped_group_ID_mapped_authors_ID = defaultdict(list)
for cat in cat_mapped_group_mapped_group_catID:
	for group, group_catID in cat_mapped_group_mapped_group_catID[cat].iteritems():
		for time in group_mapped_time[group]:
			cat_mapped_group_ID_mapped_time[cat].append((group_catID, time))
		for author in group.split(","):
			cat_mapped_group_ID_mapped_authors_ID[cat].append((group_catID, cat_mapped_authors_mapped_authors_catID[cat][author]))

logs.close()

"""
"""
cat_mapped_group_ID_mapped_time = defaultdict(list)
for cat in cat_mapped_group_mapped_group_catID:
	for group, group_catID in cat_mapped_group_mapped_group_catID[cat].iteritems():
		for time in group_mapped_time[group]:
			cat_mapped_group_ID_mapped_time[cat].append((group_catID, time))

cat_mapped_group_ID_mapped_authors_ID = defaultdict(list)
for cat in cat_mapped_group_mapped_group_catID:
	for group, group_catID in cat_mapped_group_mapped_group_catID[cat].iteritems():
		for author in group.split(","):
			cat_mapped_group_ID_mapped_authors_ID[cat].append((group_catID, cat_mapped_authors_mapped_authors_catID[cat][author]))
"""
"""
# Generate complete hypergraph and hyperedge_time
with open(output+"/hypergraph.csv", "w") as f:
	for group, ID in groups_mapped_ID.iteritems():
		hid_uid = map(lambda author: (ID, authors_mapped_ID[author]), group.split(','))
		writer = csv.writer(f)
		for tupl in hid_uid:
			writer.writerow([tupl[0], tupl[1]])

with open(output+"/hyperedge_time.csv", "w") as f:
	for group, ID in groups_mapped_ID.iteritems():
		hid_time = map(lambda time: (ID, time), group_mapped_time[group])
		writer = csv.writer(f)
		for tupl in hid_time:
			writer.writerow([tupl[0], tupl[1]])

# Generate category based hypergraph and hyperedge_time
for cat in cat_mapped_group_ID_mapped_authors_ID:
	with open(output+"/hypergraph_"+cat+".csv", "w") as f:
		writer = csv.writer(f)
		for tupl in cat_mapped_group_ID_mapped_authors_ID[cat]:
			writer.writerow([tupl[0], tupl[1]])

for cat in cat_mapped_group_ID_mapped_time:
	with open(output+"/hyperedge_time_"+cat+".csv", "w") as f:
		writer = csv.writer(f)
		for tupl in cat_mapped_group_ID_mapped_time[cat]:
			writer.writerow([tupl[0], tupl[1]])

# Store connections between complete hypergraph and category based hypergraphs
with open(output+"/authors_catID_to_ID.json", 'w') as a:
    json.dump(cat_mapped_authors_catID_mapped_authors_ID, a)

with open(output+"/groups_catID_to_ID.json", 'w') as g:
    json.dump(cat_mapped_group_catID_mapped_group_ID, g)
"""