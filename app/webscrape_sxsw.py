import requests
import bs4 
import json
import datetime
import simplejson, urllib

root_url='http://localhost:3000'
index_url=root_url+'/sxsw/sessions/'



# def check_fortune500():
# 	fortune_companies=[]
# 	companies=[]

	
# 	file=open("matched_companies.txt",'w')

# 	with open("fortune500.txt",'r') as fortune_line:
# 		for fortune in fortune_line:
# 			temp_temp_fortune=str(fortune)
# 			temp_fortune=temp_temp_fortune.lower().strip()
# 			fortune_companies.append(temp_fortune)

# 	with open("company_list.txt",'r') as line_in_file:
# 		for line in line_in_file:
# 			temp_temp_line=str(line)
# 			temp_line=temp_temp_line.lower().strip()
# 			companies.append(temp_line)

# 	for company in companies:
# 	 	for fortune in fortune_companies:
# 	  		result=fortune.find(company)
# 	  		if result!=(-1):
# 	  			file.write(company+"\n")
# 	  			break

# check_fortune500()


# def print_speakers_info():
# 	companies=[]
# 	file=open("company_list.txt",'w')
# 	with open("speakers_info.txt",'r') as line_in_file:
# 		for line in line_in_file:
# 			line_info=line.rsplit("()")
# 			temp_event=line_info[0]
# 			temp_speaker=line_info[1]
# 			temp_role=line_info[2]
# 			temp_company=line_info[3]
# 			if temp_company not in companies:
# 				companies.append(temp_company)

# 	for company in companies:
# 		temp_company=company.encode('ascii','ignore')
# 		file.write(temp_company+"\n")

# print_speakers_info()


##### INDIVIDUAL LINK TESTING #####
# def get_all_speakers():
#  	info_of_speakers=[]
#  	#load each link
#  	file=open("test.txt","w")
# 	#scrape information page of each event
# 	response=requests.get('http://localhost:3000/sxsw/sessions/event_MP991188')
# 	soup=bs4.BeautifulSoup(response.text)
# 	#getting all the information within the <pre></pre> tag
# 	json_data=json.loads(soup.pre.text)
# 	#assign value to variable only if json data exists
# 	try:
# 		if json_data['presenters'] is not None:  
# 			for presenter_info in json_data['presenters']:
# 				if presenter_info['company'] is not None:
# 					temp_company=presenter_info['company'].encode('ascii','ignore')
# 				else:
# 					temp_company="No Info"
# 				if presenter_info['role'] is not None:
# 					temp_temp_role=presenter_info['role'].strip()
# 					if not temp_temp_role:
# 						temp_role="No Info"
#  					else:
# 						temp_role=temp_temp_role.encode('ascii','ignore')
# 				if presenter_info['name'] is not None:
# 					temp_name=presenter_info['name'].encode('ascii','ignore')
# 				else:
# 					temp_name="No Info"
# 				file.write(str(temp_name)+":"+str(temp_role)+","+str(temp_company))
# 				file.write("\n")

# 	except (TypeError):
# 	 	pass
# 	file.close()

# get_all_speakers()

# def get_all_speakers():
#  	info_of_speakers=[]
#  	response=requests.get(index_url)	
#  	soup=bs4.BeautifulSoup(response.text)
#  	#load each link
#  	file=open("speakers_info.txt","w")
#  	for link in soup.find_all('a'):
#  		append_link=link.get('href')
# 	 	#scrape information page of each event
# 	 	response=requests.get(root_url+append_link)
# 	 	soup=bs4.BeautifulSoup(response.text)
# 	 	#getting all the information within the <pre></pre> tag
# 	 	json_data=json.loads(soup.pre.text)
# 	 	#assign value to variable only if json data exists
# 		try:
# 			if json_data['presenters'] is not None:  
# 				temp_speaker_event=json_data['title']
# 				speaker_event=temp_speaker_event.encode('ascii','ignore')
# 				for presenter_info in json_data['presenters']:
# 					if presenter_info['company'] is not None:
# 						temp_company=presenter_info['company'].encode('ascii','ignore')
# 					else:
# 						temp_company="No Info"
# 					if presenter_info['role'] is not None:
# 						temp_temp_role=presenter_info['role'].strip()
# 						if not temp_temp_role:
# 							temp_role="No Info"
# 	 					else:
# 							temp_role=temp_temp_role.encode('ascii','ignore')
# 					if presenter_info['name'] is not None:
# 						temp_name=presenter_info['name'].encode('ascii','ignore')
# 					else:
# 						temp_name="No Info"

# 					file.write(str(speaker_event)+"()"+str(temp_name)+"()"+str(temp_role)+"()"+str(temp_company))
# 					file.write("\n")
# 		except (TypeError):
# 		 	pass
# 	file.close()

# get_all_speakers()

# def get_all_events_type():
# 	temp_type=""
#  	all_events_type={}
#  	response=requests.get(index_url)	
#  	soup=bs4.BeautifulSoup(response.text)
#  	#load each link
#  	for link in soup.find_all('a'):
#  		append_link=link.get('href')
#  		#scrape information page of each event
#  		response=requests.get(root_url+append_link)
#  		soup=bs4.BeautifulSoup(response.text)
#  		#getting all the information within the <pre></pre> tag
#  		json_data=json.loads(soup.pre.text)
#  		#assign value to variable only if json data exists
# 	 	try:
# 	 		if (json_data['title'] is not None) and (json_data['type'] is not None):  
# 		 		temp_event=json_data['title']
# 		 		temp_type_list=json_data['type']
# 		 		if len(temp_type_list)>0:
# 			 		if len(temp_type_list)>1:
# 			 			temp_type=','.join(temp_type_list)
# 			 			all_events_type[temp_event]=temp_type
# 			 		else:
# 			 			temp_type=''.join(temp_type_list)
# 			 			all_events_type[temp_event]=temp_type
# 		 		else:
# 		 			all_events_type[temp_event]="No Type"
# 	 	except (TypeError):
# 	 		pass

#  	if all_events_type:
#  		file=open("type.txt","w")
#  		for event_info in all_events_type:
#  			event_info_encode=event_info.encode('ascii','ignore')
#  			type_info_encode=all_events_type[event_info].encode('ascii','ignore')
#  			file.write(event_info_encode+":"+type_info_encode+"\n")
#  		file.close()


# get_all_events_type()

			
# def get_all_events_timings():
#  	all_events_timings={}
#  	response=requests.get(index_url)	
#  	soup=bs4.BeautifulSoup(response.text)
#  	#load each link
#  	for link in soup.find_all('a'):
#  		append_link=link.get('href')
#  		#scrape information page of each event
#  		response=requests.get(root_url+append_link)
#  		soup=bs4.BeautifulSoup(response.text)
#  		#getting all the information within the <pre></pre> tag
#  		json_data=json.loads(soup.pre.text)
#  		#assign value to variable only if json data exists
#  		try:
#  			if (json_data['starts_at'] is not None) and (json_data['ends_at'] is not None) and (json_data['title'] is not None):  
#  				temp_event=json_data['title']
#  				temp_start=json_data['starts_at']
#  				temp_end=json_data['ends_at']
#  				#add the event and timing to list if it doesn't already exist
#  				if temp_event not in all_events_timings:
#  					all_events_timings[temp_event]=(temp_start, temp_end)
#  		except (TypeError):
#  			pass
#  	if all_events_timings:
#  		file=open("events_timings.txt","w")
#  		for event_info in all_events_timings:
#  			event_info_encode=event_info.encode('ascii','ignore')
#  			file.write(str(event_info_encode)+":"+str(all_events_timings[event_info])+"\n")
#  		file.close()
	
# get_all_events_timings()

# def get_all_venues_events():
# 	all_venues_events={}
# 	response=requests.get(index_url)	
# 	soup=bs4.BeautifulSoup(response.text)
# 	#load each link
# 	for link in soup.find_all('a'):
# 		append_link=link.get('href')
# 		#scrape information page of each event
# 		response=requests.get(root_url+append_link)
# 		soup=bs4.BeautifulSoup(response.text)
# 		#getting all the information within the <pre></pre> tag
# 		json_data=json.loads(soup.pre.text)
# 		#assign value to variable only if json data exists
# 		try:
# 			if (json_data['location']['venue'] is not None) and (json_data['title'] is not None):  
# 				temp_venue=json_data['location']['venue']
# 				temp_event=json_data['title']
# 				#add the venue and its coords to list if it doesn't already exist
# 				if temp_event not in all_venues_events:
# 					all_venues_events[temp_event]=temp_venue
# 		except (TypeError):
# 			pass
# 	if all_venues_events:
# 		file=open("venues_events.txt","w")
# 		for event_info in all_venues_events:
# 			event_info_encode=event_info.encode('ascii','ignore')
# 			venue_info_encode=all_venues_events[event_info].encode('ascii','ignore')
# 			file.write(str(event_info_encode)+":"+str(venue_info_encode)+"\n")
# 		file.close()
	

# get_all_venues_events()

# def get_all_venues_coords():
# 	all_venues_coords={}
# 	response=requests.get(index_url)	
# 	soup=bs4.BeautifulSoup(response.text)
# 	#load each link
# 	for link in soup.find_all('a'):
# 		append_link=link.get('href')
# 		#scrape information page of each event
# 		response=requests.get(root_url+append_link)
# 		soup=bs4.BeautifulSoup(response.text)
# 		#getting all the information within the <pre></pre> tag
# 		json_data=json.loads(soup.pre.text)
# 		#assign value to variable only if json data exists
# 		try:
# 			if (json_data['location']['venue'] is not None) and (json_data['coordinates']['latitude'] is not None) and (json_data['coordinates']['longitude'] is not None):  
# 				temp_venue=json_data['location']['venue']
# 				temp_lat=json_data['coordinates']['latitude']
# 				temp_long=json_data['coordinates']['longitude']
# 				#add the venue and its coords to list if it doesn't already exist
# 				if temp_venue not in all_venues_coords:
# 					all_venues_coords[temp_venue]=(temp_lat,temp_long)
# 		except (TypeError):
# 			pass
		
# 	if all_venues_coords:
# 		file=open("coordinates.txt","w")
# 		for coord_info in all_venues_coords:
# 			file.write(str(coord_info)+":"+str(all_venues_coords[coord_info])+"\n")
# 		file.close()
	

# get_all_venues_coords()

# def get_all_venues_coords():
# 	all_venues_coords={}
# 	response=requests.get("http://localhost:3000/sxsw/sessions/event_IAP40059")
# 	soup=bs4.BeautifulSoup(response.text)
# 	#getting all the information within the <pre></pre> tag
# 	json_data=json.loads(soup.pre.text)
# 	#before doing anything check that none of the fields are none
# 	if json_data['location']['venue'] != None and json_data['coordinates']['latitude'] != None and json_data['coordinates']['longitude'] != None:
# 		temp_venue=json_data['location']['venue']
# 		temp_lat=json_data['coordinates']['latitude']
# 		temp_long=json_data['coordinates']['longitude']
# 		#add the venue to list if it doesn't already exist
# 		if temp_venue not in all_venues_coords:
# 			all_venues_coords[temp_venue]=(temp_lat,temp_long)
# 	if all_venues_coords:
# 		file=open("coordinates.txt","w")
# 		for coord_info in all_venues_coords:
# 			file.write(str(coord_info)+":"+str(all_venues_coords[coord_info])+"\n")
# 		file.close()

# get_all_venues_coords()


# def write_all_venues_to_file():
# 	all_venues=[]
# 	response=requests.get(index_url)	
# 	soup=bs4.BeautifulSoup(response.text)
# 	for link in soup.find_all('a'):
# 		append_link=link.get('href')
# 		#scrape information page of each event
# 		response=requests.get(root_url+append_link)
# 		soup=bs4.BeautifulSoup(response.text)
# 		#getting all the information within the <pre></pre> tag
# 		json_data=json.loads(soup.pre.text)
# 		temp_venue=json_data['location']['venue']
# 		#add the venue to list if it doesn't already exist
# 		if temp_venue not in all_venues:
# 			all_venues.append(temp_venue)
# 		#write all values in list to file
# 		file=open("venues.txt","w")
# 	for venue in all_venues:
# 		file.write(str(venue)+"\n")
# 	file.close()

# def write_all_events_to_file():
#  	all_events=[]
#  	response=requests.get(index_url)	
#  	soup=bs4.BeautifulSoup(response.text)
#  	for link in soup.find_all('a'):
#  		append_link=link.get('href')
#  		#scrape information page of each event
#  		response=requests.get(root_url+append_link)
#  		soup=bs4.BeautifulSoup(response.text)
#  		#getting all the information within the <pre></pre> tag
#  		json_data=json.loads(soup.pre.text)
#  		temp_event=json_data['title']
#  		#add the venue to list if it doesn't already exist
#  		if temp_event not in all_events:
#  			all_events.append(temp_event)
#  		#write all values in list to file
#  		file=open("events.txt","w")
#  	for event in all_events:
#  		event_encode=event.encode('ascii','ignore')
#  		file.write(str(event_encode)+"\n")
#  	file.close()

# write_all_events_to_file()