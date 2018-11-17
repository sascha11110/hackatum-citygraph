#!/usr/bin/python3

import sys, re, requests, string, json

def send_request(filename, get = '', post = {}):
	return requests.post('https://www.ris-muenchen.de/RII/RII/' + filename + '.jsp?' + get, data=post).text

def get_all_proposal_ids(ids_filename):
	ids = []
	txtpos = 0
	id_file = open(ids_filename, 'w')
	while True:
		response = send_request('ris_antrag_trefferliste', 'nav=1', {'txtPosition': txtpos, 'txtVon': '01.01.2001'})
		new_ids = re.findall('ris_antrag_detail\.jsp\?risid=([0-9]+)', response, re.S)
		print('crawled the following new ids:\n' + str(new_ids))
		id_file.write('\n'.join(new_ids) + '\n') # put every id in a new line
		if len(new_ids) < 10: # if less than 10 ids are returned, we reached the last page
			break
		ids = ids + new_ids
		txtpos = txtpos + 10
	id_file.close()
	return ids

def get_all_proposals(ids_filename, proposals_filename):
	id_file = open(ids_filename, 'r')
	result_file = open(proposals_filename, 'w')
	result_file.write('[\n')
	line = id_file.readline()
	while True:
		results = get_proposal_details(int(line))
		print('proposal with id ' + line.strip() + ':\n' + str(results))
		json.dump(results, result_file, sort_keys=True, indent=4, ensure_ascii=False)
		line = id_file.readline()
		if not line:
			id_file.close()
			break
		result_file.write(',\n')
	result_file.write('\n]\n')
	result_file.close()

def get_proposal_details(id):
	response = send_request('ris_antrag_detail', 'risid=' + str(id))
	details = re.findall('<div class="detail_div">(.*?)</div>', response, re.S)
	details_left =  re.findall('<div class="detail_div_left">(.*?)</div>', response, re.S)
	details_right =  re.findall('<div class="detail_div_right">(.*?)</div>', response, re.S)
	details_left_long =  re.findall('<div class="detail_div_left_long">(.*?)</div>', response, re.S)
	if len(details) > 2: # editing information is not always present
		editing = re.findall('</span>(.*?)\r\n', details[2], re.S)[0]
	else:
		editing = None
	if len(details_left_long) > 2: # done date is only present on finished proposals
		done_date = details_left_long[2]
	else:
		done_date = None
	proposal = {
		'id': id,
		'subject': details[0],
		'status': details[1],
		'editing': editing,
		'type': details_left[0],
		'proposal_date': details_left[1],
		'processing_period': details_left[2],
		'department': details_right[0],
		'legislative_period': details_right[1],
		'proposal_by': details_left_long[0],
		'done_date': done_date,
		'documents': get_proposal_documents(id),
		'results': get_proposal_results(id)
	}
	return proposal

def get_proposal_documents(id):
	response = send_request('ris_antrag_dokumente', 'risid=' + str(id))
	document_details = re.findall('href="/RII/RII/DOK/ANTRAG/([0-9]*?)\.pdf">(.*?)</a>', response, re.S)
	documents = []
	for document_detail in document_details:
		documents.append({
			'name': document_detail[1],
			'url': 'https://www.ris-muenchen.de/RII/RII/DOK/ANTRAG/' + document_detail[0] + '.pdf'
		})
	return documents

def get_proposal_results(id):
	results = send_request('ris_antrag_ergebnisse', 'risid=' + str(id))
	rows = re.findall('<tr class="ergebnistab_tr">(.*?)</tr>', results, re.S)
	results = []
	for row in rows:
		cols = re.findall('<td class="[a-z\s]*">(.*?)</td>', row, re.S)
		if cols[4] == '&nbsp;': # skip results which have an empty description
			continue
		gremium = re.findall('ris_gremien_detail.jsp\?risid=([0-9]+?)&periodeid=([0-9]+?)">(.*?)</a>', cols[0], re.S)
		if len(gremium) > 0: # sometimes there are ba_gremien instead of ris_gremien
			gremium = gremium[0]
		else:
			gremium = re.findall('ba_gremien_details.jsp\?Id=([0-9]+?)&Wahlperiode=([0-9]+?)" target="_blank">(.*?)</a>', cols[0], re.S)[0]
		setting_date = re.findall('ris_sitzung_detail.jsp\?risid=([0-9]+)">([0-9]{2}\.[0-9]{2}\.[0-9]{4}), ([0-9]{2}:[0-9]{2})</a>', cols[1], re.S)
		if len(setting_date) > 0: # sometimes there are ba_sitzungen instead of ris_sitzungen
			setting_date = setting_date[0]
		else:
			setting_date = re.findall('ba_sitzungen_details.jsp\?Id=([0-9]+)" target="_blank">([0-9]{2}\.[0-9]{2}\.[0-9]{4}), ([0-9]{2}:[0-9]{2})</a>', cols[1], re.S)[0]
		template = re.findall('ris_vorlagen_detail.jsp\?risid=([0-9]+)">(.*?)</a>', cols[3], re.S)[0]
		resolution_file = re.findall('href="/RII/RII/DOK/TOP/([0-9]+)\.pdf"', cols[3], re.S)[0]
		results.append({
			'committee_id': gremium[0],
			'committee_legislative_period': gremium[1],
			'committee_name': gremium[2],
			'result_date': setting_date[0],
			'result_time': setting_date[1],
			'template_id': template[0],
			'template_num': template[1],
			'resolution_file': 'https://www.ris-muenchen.de/RII/RII/DOK/ANTRAG/' + resolution_file + '.pdf',
			'result_description': cols[4]
		})
	return results

def main(args):
	
	# filenames
	ids_filename = 'ids.txt'
	proposals_filename = 'proposals.json'
	
	# get all proposal ids
	#ids = get_all_proposal_ids(ids_filename)
	#print('crawled' + str(len(ids)) + ' ids')
	
	# get all proposal details
	proposals = get_all_proposals(ids_filename, proposals_filename)
	print('crawled' + str(len(proposals)) + ' proposal details')


if __name__ == '__main__':
	main(sys.argv)
