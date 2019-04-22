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
							group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','').lower()) for author in authors])).strip(",| ")
							
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
					group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','').lower()) for author in authors])).strip(",| ")

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
					for cat in categories_mapped_journal:
						if venue in categories_mapped_journal[cat]:
							group = ",".join(sorted([remove_accents(author.lower()) for author in a[7].strip(",| ").split(",")]))

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


def pubmed_complete():
	# These three dictionaries are required by the SimpleHypergraph class
	authors_set = set()
	group_mapped_time = defaultdict(set)

	count = 0
	end = end_year-start_year + 1
	printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
	for year in range(start_year, end_year+1):
		for line in open(dataset+"/pubmed_"+str(year)+".txt"):
			a = line.strip().split('\t')
			if a[7] != '':
				try:
					time = datetime.strptime(a[1].strip(), '%Y/%m/%d %H:%M')
					group = ",".join(sorted([remove_accents(author.lower()) for author in a[7].strip(",| ").split(",")]))
					
					group_mapped_time[group].add(time)
					authors_set.update(group.split(","))
				except:
					error.write(line+'\n')
		count += 1
		printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

	dblp = SimpleHypergraph(group_mapped_time, authors_set, output)
	dblp.generate_complete_hypergraph()

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