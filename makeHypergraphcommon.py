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
							group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','').lower()) for author in authors if author != ''])).strip(",| ")
							
							group_mapped_time[group].add(time)
							cat_mapped_groups[cat].add(group)
							cat_mapped_authors[cat].update([author for author in group.split(",")])
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
					group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','').lower()) for author in authors if author != ''])).strip(",| ")

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
							group = ",".join(sorted([remove_accents(author.lower()) for author in a[7].strip(",| ").split(",") if author != '']))

							group_mapped_time[group].add(time)
							cat_mapped_groups[cat].add(group)
							cat_mapped_authors[cat].update([author for author in group.split(",")])
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
		for line in open(dataset+"/test_pubmed.txt"):
			a = line.strip().split('\t')
			if a[7] != '':
				try:
					time = datetime.strptime(a[1].strip(), '%Y/%m/%d %H:%M')
					group = ",".join(sorted([remove_accents(author.lower()) for author in a[7].strip(",| ").split(",") if author != '']))
					
					group_mapped_time[group].add(time)
					authors_set.update(group.split(","))
				except:
					error.write(line+'\n')
		count += 1
		printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

	pubmed = SimpleHypergraph(group_mapped_time, authors_set, output)
	pubmed.generate_complete_hypergraph()

def USPatent():
	cat_mapped_authors = defaultdict(set)
	cat_mapped_groups = defaultdict(set)
	group_mapped_time = defaultdict(set)

	patID_mapped_group = defaultdict(set)
	for line in open(dataset+"/ainventor.txt", "r+"):
		patID = line.split(',')[0]
		try:
			author = line.split(',')[2].strip('"') + " " + line.split(',')[1].strip('"')
			patID_mapped_group[patID].add(author)
		except:
			error.write(line+'\n')

	for line in open(dataset+"/apat63_99.txt", "r+"):
		patID = line.split(',')[0]
		dt = int(line.split(',')[1])
		if dt >= start_year and dt <= end_year:
			time = str(dt)
			cat = line.split(',')[10]
			if cat != '6':
				group = ",".join(sorted([remove_accents(author.lower()) for author in patID_mapped_group[patID] if author != '']))

				group_mapped_time[group].add(time)
				cat_mapped_groups[cat].add(group)
				cat_mapped_authors[cat].update([author for author in group.split(",")])
				
	uspatent = CategoryBasedHypergraph(group_mapped_time, cat_mapped_authors, cat_mapped_groups, output)
	uspatent.generate_complete_hypergraph()
	uspatent.generate_category_based_hypergraph()

def USPatent_complete():
	# These three dictionaries are required by the SimpleHypergraph class
	authors_set = set()
	group_mapped_time = defaultdict(set)

	patID_mapped_group = defaultdict(set)
	for line in open(dataset+"/ainventor.txt", "r+"):
		patID = line.split(',')[0]
		try:
			author = line.split(',')[2].strip('"') + " " + line.split(',')[1].strip('"')
			patID_mapped_group[patID].add(author)
		except:
			error.write(line+'\n')

	for line in open(dataset+"/apat63_99.txt", "r+"):
		patID = line.split(',')[0]
		dt = int(line.split(',')[1])
		if dt >= start_year and dt <= end_year:
			time = str(dt)
			cat = line.split(',')[10]
			if cat != '6':
				group = ",".join(sorted([remove_accents(author.lower()) for author in patID_mapped_group[patID] if author != '']))

				group_mapped_time[group].add(time)
				authors_set.update(group.split(","))

	uspatent = SimpleHypergraph(group_mapped_time, authors_set, output)
	uspatent.generate_complete_hypergraph()

def arxiv():
	cat_mapped_authors = defaultdict(set)
	cat_mapped_groups = defaultdict(set)
	group_mapped_time = defaultdict(set)

	data_folders = os.listdir(dataset)
	count = 0
	end = len(data_folders)
	printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
	for folder in range(end):
		cat = data_folders[folder]
		for line in open(dataset+"/"+data_folders[folder]+"/"+data_folders[folder]+".txt", "r+"):
			try:
				a = line.strip().split('\t')
				dt = datetime.strptime(a[2].strip(), '%Y-%m')
				if dt.year >= start_year and dt.year <= end_year:
					time = dt.strftime('%Y%m%d')
					authors = a[4].split("|")
					group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','').lower()) for author in authors if author != ''])).strip(",| ")
					
					group_mapped_time[group].add(time)
					cat_mapped_groups[cat].add(group)
					cat_mapped_authors[cat].update([author for author in group.split(",")])
			except:
				error.write(line+'\n')
		count += 1
		printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
	
	arxiv = CategoryBasedHypergraph(group_mapped_time, cat_mapped_authors, cat_mapped_groups, output)
	arxiv.generate_complete_hypergraph()
	arxiv.generate_category_based_hypergraph()

def arxiv_complete():
	# These three dictionaries are required by the SimpleHypergraph class
	authors_set = set()
	group_mapped_time = defaultdict(set)

	data_folders = os.listdir(dataset)
	count = 0
	end = len(data_folders)
	printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
	for folder in range(end):
		cat = data_folders[folder]
		for line in open(dataset+"/"+data_folders[folder]+"/"+data_folders[folder]+".txt", "r+"):
			try:
				a = line.strip().split('\t')
				dt = datetime.strptime(a[2].strip(), '%Y-%m')
				if dt.year >= start_year and dt.year <= end_year:
					time = dt.strftime('%Y%m%d')
					authors = a[4].split("|")
					group = ",".join(sorted([remove_accents(author.strip(",| ").replace(',','').lower()) for author in authors if author != ''])).strip(",| ")
					
					group_mapped_time[group].add(time)
					authors_set.update(group.split(","))
			except:
				error.write(line+'\n')
		count += 1
		printProgress(count, end, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

	arxiv = SimpleHypergraph(group_mapped_time, authors_set, output)
	arxiv.generate_complete_hypergraph()

def eumail_complete():
	# These three dictionaries are required by the SimpleHypergraph class
	authors_set = set()
	group_mapped_time = defaultdict(set)

	f = open(dataset+'/email-Eu-full-nverts.txt','r+')
	g = open(dataset+'/email-Eu-full-simplices.txt','r+')
	h = open(dataset+'/email-Eu-full-times.txt','r+')
	try:
		for nvert in f:
			n = nvert.replace('\n','')
			authors_group = []
			for i in range(int(n)):
				author = g.readline().replace('\n','')
				authors_set.add(author)
				authors_group.append(author)
			group = ','.join(sorted(authors_group))
			time = h.readline().replace('\n','')
			group_mapped_time[group].add(time)
	except:
		error.write(line+'\n')

	eumail = SimpleHypergraph(group_mapped_time, authors_set, output)
	eumail.generate_complete_hypergraph()

def imdb():
	cat_mapped_authors = defaultdict(set)
	cat_mapped_groups = defaultdict(set)
	group_mapped_time = defaultdict(set)

	patID_mapped_group = defaultdict(set)
	for line in open(dataset+"/principals.tsv", "r+"):
		values = line.replace('\n','').split('\t')
		patID = values[0]
		try:
			author = values[2]
			patID_mapped_group[patID].add(author)
		except:
			error.write(line+'\n')

	for line in open(dataset+"/basics.tsv", "r+"):
		values = line.replace('\n','').split('\t')
		patID = values[0]
		try:
			dt = int(values[5])
			if dt >= start_year and dt <= end_year:
				time = str(dt)
				#subcat = line.split(',')[11]
				categories = values[8]
				group = ",".join(sorted([remove_accents(author.lower()) for author in patID_mapped_group[patID] if author != '']))

				group_mapped_time[group].add(time)
				for cat in categories.split(','):
					cat_mapped_groups[cat].add(group)
					cat_mapped_authors[cat].update([author for author in group.split(",")])
		except:
			error.write(line+'\n')

	imdb = CategoryBasedHypergraph(group_mapped_time, cat_mapped_authors, cat_mapped_groups, output)
	imdb.generate_complete_hypergraph()
	imdb.generate_category_based_hypergraph()

def imdb_complete():
	# These three dictionaries are required by the SimpleHypergraph class
	authors_set = set()
	group_mapped_time = defaultdict(set)

	patID_mapped_group = defaultdict(set)
	for line in open(dataset+"/principals.tsv", "r+"):
		values = line.replace('\n','').split('\t')
		patID = values[0]
		try:
			author = values[2]
			patID_mapped_group[patID].add(author)
		except:
			error.write(line+'\n')

	for line in open(dataset+"/basics.tsv", "r+"):
		values = line.replace('\n','').split('\t')
		patID = values[0]
		try:
			dt = int(values[5])
			if dt >= start_year and dt <= end_year:
				time = str(dt)
				group = ",".join(sorted([remove_accents(author.lower()) for author in patID_mapped_group[patID] if author != '']))

				group_mapped_time[group].add(time)
				authors_set.update(group.split(","))
		except:
			error.write(line+'\n')

	imdb = SimpleHypergraph(group_mapped_time, authors_set, output)
	imdb.generate_complete_hypergraph()

if __name__ == '__main__':

	args = sys.argv
	output_type = args[1]
	dataset = args[2]
	start_year = int(args[3])
	end_year = int(args[4])
	output = args[5]
	#if output_type == "category":
	#	support = args[6]
	
	# Check if output folder exists
	output += "_"+str(start_year)+"_"+str(end_year)
	if not os.path.exists(output):
		os.makedirs(output)
	else:
		shutil.rmtree(output)
		os.makedirs(output)

	error = open(output+"/error.txt", "w")
	eumail_complete()
	error.close()
