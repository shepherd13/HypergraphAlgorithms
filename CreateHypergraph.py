import csv
import json
from collections import defaultdict
import os

class SimpleHypergraph:
	def __init__(self, group_mapped_time, authors_set, path):
		self.group_mapped_time = group_mapped_time
		self.path = path
		self.logs = open(path+"/logs.txt", "w")
		self.groups_mapped_ID = self.mapID(self.group_mapped_time.keys(), 1)	# Map all co-author groups to ID's
		self.authors_mapped_ID = self.mapID(authors_set, 1)						# Map all authors to ID's

	def mapID(self, sequence, start):
		dictionary = dict(enumerate(sequence, start))
		reverse_dictionary = dict((v, k) for k, v in dictionary.iteritems())
		return reverse_dictionary
	
	def write_tuples(self, file_path, tuple_list):
		with open(file_path, "w") as f:
			writer = csv.writer(f)
			for tupl in tuple_list:
				writer.writerow([tupl[0], tupl[1]])

	def generate_complete_hypergraph(self):
		path = self.path+"/complete"
		os.mkdir(path)

		hid_uid = []
		for group, ID in self.groups_mapped_ID.iteritems():
			hid_uid.extend(map(lambda author: (ID, self.authors_mapped_ID[author]), group.split(',')))
		self.write_tuples(path+"/hypergraph.csv", hid_uid)
		hid_time = []
		for group, ID in self.groups_mapped_ID.iteritems():
			hid_time.extend(map(lambda time: (ID, time), self.group_mapped_time[group]))
		self.write_tuples(path+"/hyperedge_time.csv", hid_time)
		
		self.logs.write("Total authors in complete hypergraph : " +str(len(self.authors_mapped_ID)) + "\n")
		self.logs.write("Total hyperedges in complete hypergraph : " +str(len(self.groups_mapped_ID)) + "\n")

	def __del__(self):
		self.logs.close()


class CategoryBasedHypergraph(SimpleHypergraph):
	def __init__(self, group_mapped_time, cat_mapped_authors, cat_mapped_groups, path):
		self.cat_mapped_authors = cat_mapped_authors
		self.cat_mapped_groups = cat_mapped_groups

		authors_set = reduce(lambda a,s: a|s, self.cat_mapped_authors.values(),set())
		SimpleHypergraph.__init__(self, group_mapped_time, authors_set, path)

	def generate_category_based_hypergraph(self):
		# Map category based authors to ID
		cat_mapped_authors_mapped_authors_catID = defaultdict(dict)
		cat_mapped_authors_catID_mapped_authors_ID = defaultdict(dict)
		for cat, authors in self.cat_mapped_authors.iteritems():
			cat_mapped_authors_mapped_authors_catID[cat] = self.mapID(authors, 1)
			for author, author_catID in cat_mapped_authors_mapped_authors_catID[cat].iteritems():
				cat_mapped_authors_catID_mapped_authors_ID[cat][author_catID] = self.authors_mapped_ID[author]
			self.logs.write("Total authors in category " + str(cat) + " : " +str(len(self.cat_mapped_authors[cat])) + "\n")

		# Map category based co-author groups to ID
		cat_mapped_group_mapped_group_catID = defaultdict(dict)
		cat_mapped_group_catID_mapped_group_ID = defaultdict(dict)
		for cat, groups in self.cat_mapped_groups.iteritems():
			cat_mapped_group_mapped_group_catID[cat] = self.mapID(groups, 1)
			for group, group_catID in cat_mapped_group_mapped_group_catID[cat].iteritems():
				cat_mapped_group_catID_mapped_group_ID[cat][group_catID] = self.groups_mapped_ID[group]
			self.logs.write("Total hyperedges in category " + str(cat) + " : " + str(len(self.cat_mapped_groups[cat])) + "\n")

		# Map category based hyperedge ID to time and hyperedge ID to authors ID
		cat_mapped_group_ID_mapped_time = defaultdict(list)
		cat_mapped_group_ID_mapped_authors_ID = defaultdict(list)
		for cat in cat_mapped_group_mapped_group_catID:
			for group, group_catID in cat_mapped_group_mapped_group_catID[cat].iteritems():
				for time in self.group_mapped_time[group]:
					cat_mapped_group_ID_mapped_time[cat].append((group_catID, time))
				for author in group.split(","):
					cat_mapped_group_ID_mapped_authors_ID[cat].append((group_catID, cat_mapped_authors_mapped_authors_catID[cat][author]))
		path = self.path+"/category_based"
		os.mkdir(path)
		# Generate category based hypergraph and hyperedge_time
		for cat in cat_mapped_group_ID_mapped_authors_ID:
			self.write_tuples(path+"/hypergraph_"+cat+".csv", cat_mapped_group_ID_mapped_authors_ID[cat])
		for cat in cat_mapped_group_ID_mapped_time:
			self.write_tuples(path+"/hyperedge_time_"+cat+".csv", cat_mapped_group_ID_mapped_time[cat])
			
		# Store connections between complete hypergraph and category based hypergraphs
		with open(path+"/authors_catID_to_ID.json", 'w') as a:
			json.dump(cat_mapped_authors_catID_mapped_authors_ID, a)
		with open(path+"/groups_catID_to_ID.json", 'w') as g:
			json.dump(cat_mapped_group_catID_mapped_group_ID, g)

	def __del__(self):
		SimpleHypergraph.__del__(self)
