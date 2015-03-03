from forms import locationSelectionForm
from geopy.distance import vincenty
from time import strftime, strptime
import datetime
import requests
import bs4 
import json
import simplejson, urllib

def show_recommendations(current_loc, current_next_event):
	message="SUCCESS"
	current_next_event_venue=""
	current_next_event_start_date_time_string=""
	possible_future_events={}
	possible_future_events_SCORE={}
	possible_future_events_final=[]
	possible_future_events_TYPE=[]
	possible_event_added=0
	highest_score=0.0
	highest_event=""
	number_of_presenters={}

	#venue:coords
	venues_coords={}
	with open("coordinates.txt",'r') as line_in_file:
		for line in line_in_file:
			venue_in_line=line.split(":",1)[0]
			coords_in_line=line.split(":",1)[1]
			venues_coords[venue_in_line]=coords_in_line

	#venue:event
	venues_events={}
	with open("venues_events.txt",'r') as line_in_file:
		for line in line_in_file:
			event_in_line,venue_in_line=line.rsplit(":",1)
			venues_events[event_in_line]=venue_in_line

	#event:timing
	events_timings={}
	with open("events_timings.txt",'r') as line_in_file:
		for line in line_in_file:
			event_in_line_temp,timing_in_line_temp=line.rsplit("(",1)
			event_in_line,dont_want_temp=event_in_line_temp.rsplit(":",1)
			timing_in_line="("+str(timing_in_line_temp)
			events_timings[event_in_line]=timing_in_line
	
	#event:type
	events_type={}
	with open("type.txt",'r') as line_in_file:
		for line in line_in_file:
			event_in_line,type_in_line=line.rsplit(":",1)
			events_type[event_in_line]=type_in_line

	#company:fortune500 rank
	fortune_companies={}
	with open("matched_companies.txt",'r') as line_in_file:
		for line in line_in_file:
			rank=line.split(",",1)[0]
			company=line.split(",",1)[1]
			fortune_companies[company]=rank

	#event:speaker,role,company
	speaker_info={}
	with open("speakers_info.txt",'r') as line_in_file:
		for line in line_in_file:
			event=line.split("()",1)[0]
			speaker=line.split("()",1)[1].split("()",1)[0]
			role=line.split("()",1)[1].split("()",1)[1].split("()",1)[0]
			company=line.split("()",1)[1].split("()",1)[1].split("()",1)[1]
			if event in speaker_info:
				speaker_info[event].append((speaker,role,company))
			else:
				speaker_info[event]=[(speaker,role,company)]

	#get the coords of the user's current location
	current_loc_coords=venues_coords.get(current_loc)

	#get user's current date and time in 24-hours format 
	current_time=datetime.datetime.now()

	#get the coords of the user's next event
	for venue in venues_events:
		#find the venue of the user's next event
		if venues_events[venue]==current_next_event:
			current_next_event_venue=venue
	current_next_event_coords=venues_coords.get(current_next_event_venue)

	#get the start date and timing of user's selected next event
	for events_timings_event in events_timings:
		if events_timings_event==current_next_event:
			brackets_timings=events_timings[events_timings_event]
			no_brackets_timings=brackets_timings[brackets_timings.find("(")+1:brackets_timings.find(")")]
			remove_apostrophe=no_brackets_timings.replace("'","")
			remove_u=remove_apostrophe.replace("u","")
			remove_T_timings=remove_u.replace("T"," ")
			remove_GMT_timings=remove_T_timings.replace("+08:00","")
			start_day_time_string,end_day_time_string_leadingspace=remove_GMT_timings.split(",")
			#set start date and timing of user's selected next event in String
			current_next_event_start_date_time_string=start_day_time_string

	#find all the events with timings with start time after current time and end time before next event's start time
	for events_timings_event in events_timings:
		brackets_timings=events_timings[events_timings_event]
		no_brackets_timings=brackets_timings[brackets_timings.find("(")+1:brackets_timings.find(")")]
		remove_apostrophe=no_brackets_timings.replace("'","")
		remove_u=remove_apostrophe.replace("u","")
		remove_T_timings=remove_u.replace("T"," ")
		remove_GMT_timings=remove_T_timings.replace("+08:00","")
		start_day_time_string,end_day_time_string_leadingspace=remove_GMT_timings.split(",")
		end_day_time_string=end_day_time_string_leadingspace.lstrip()
		#get the start date and time in datetime object
		start_day_time_datetime=datetime.datetime.strptime(start_day_time_string,"%Y-%m-%d %H:%M:%S")
		#get the end date and time in datetime object
		end_day_time_datetime=datetime.datetime.strptime(end_day_time_string,"%Y-%m-%d %H:%M:%S")
		current_next_event_start_datetime=datetime.datetime.strptime(current_next_event_start_date_time_string,"%Y-%m-%d %H:%M:%S")
		#only get the events which start after current timing and ends before the user's next event
		if start_day_time_datetime>current_time and end_day_time_datetime<current_next_event_start_datetime:
			#check if event has valid location info, if not dont add to possible future events list
			
			if events_timings_event in venues_events:
				venue=venues_events[events_timings_event]
				for venues in venues_coords:
					if venue.strip(" \n")==venues.strip(" \n"): 
						#add event and start timing to list dictionary of possible future events
						possible_future_events.update({events_timings_event:start_day_time_datetime})
						possible_event_added+=1

	##### calculate score for type attribute for each event in possible_future_events ####
	if possible_event_added>0:
		type_weightage=0.4
		num_presenters_weightage=0.4
		company_weightage=0.2
		travellingtime_weightage=0.4
		# ## for each possible event happening during the in-between time period, get a score based on their type ##
		for possible_future_events_event in possible_future_events:
			temp_type_unstripped=events_type[possible_future_events_event]
			temp_type=temp_type_unstripped.strip(' \n')
			### 3: Future15, 2: Others 1: No type stated ###
			if temp_type=="Future15":
				temp_score_unrounded=type_weightage*3
				temp_score=round(temp_score_unrounded,1)
				possible_future_events_SCORE[possible_future_events_event]=temp_score
			elif temp_type=="No Type":
				temp_score_unrounded=type_weightage*1
				temp_score=round(temp_score_unrounded,1)
				possible_future_events_SCORE[possible_future_events_event]=temp_score
			else:
				#any other types than Future15
				temp_score_unrounded=type_weightage*2
				temp_score=round(temp_score_unrounded,1)
				possible_future_events_SCORE[possible_future_events_event]=temp_score


		## for each possible event happening during the in-between time period, get a score based on number of speakers ##
		for possible_future_events_event in possible_future_events:
			#for each possible event, check how many speakers there are
			num_speakers=0
			#event that speaker is speaking for
			for info in speaker_info:
				#if the possible future event matches the event that the speaker is speaking for
				if possible_future_events_event==info:
					#counts the number of speakers for the event
					for speaker in speaker_info[info]:
						num_speakers+=1
			number_of_presenters[possible_future_events_event]=num_speakers
		#calculate score for events based on number of presenters
		for number_of_presenters_event in number_of_presenters:
			if number_of_presenters[number_of_presenters_event]==1:
				temp_score_unrounded=num_presenters_weightage*3
				temp_score=round(temp_score_unrounded,1)
				for possible_future_events_SCORE_event in possible_future_events_SCORE:
					if number_of_presenters_event==possible_future_events_SCORE_event:
						saved_score=possible_future_events_SCORE[possible_future_events_SCORE_event]
						new_score=saved_score+temp_score
						possible_future_events_SCORE[possible_future_events_SCORE_event]=new_score
				#possible_future_events_SCORE[number_of_presenters_event]=temp_score
			elif number_of_presenters[number_of_presenters_event]==2:
				temp_score_unrounded=num_presenters_weightage*2
				temp_score=round(temp_score_unrounded,1)
				for possible_future_events_SCORE_event in possible_future_events_SCORE:
					if number_of_presenters_event==possible_future_events_SCORE_event:
						saved_score=possible_future_events_SCORE[possible_future_events_SCORE_event]
						new_score=saved_score+temp_score
						possible_future_events_SCORE[possible_future_events_SCORE_event]=new_score
				#possible_future_events_SCORE[number_of_presenters_event]=temp_score
			else:
				temp_score_unrounded=num_presenters_weightage*1
				temp_score=round(temp_score_unrounded,1)
				for possible_future_events_SCORE_event in possible_future_events_SCORE:
					if number_of_presenters_event==possible_future_events_SCORE_event:
						saved_score=possible_future_events_SCORE[possible_future_events_SCORE_event]
						new_score=saved_score+temp_score
						possible_future_events_SCORE[possible_future_events_SCORE_event]=new_score
				#possible_future_events_SCORE[number_of_presenters_event]=temp_score

		## for each possible event, calculate score based on whether company is a Fortune500 company ##
		for possible_future_events_event in possible_future_events:
			#find the speakers for each event and check their company
			for event in speaker_info:
				if possible_future_events_event==event:
					event_company_score=0
					#looping through each presenter info for a particular event
					for event_info in speaker_info[event]:
						if event_info[2].lower() in fortune_companies:
							temp_score_unrounded=company_weightage*1
						else:
							temp_score_unrounded=company_weightage*0
						temp_score=round(temp_score_unrounded,1)
						event_company_score+=temp_score
						for possible_future_events_SCORE_event in possible_future_events_SCORE:
							if event==possible_future_events_SCORE_event:
								saved_score=possible_future_events_SCORE[possible_future_events_SCORE_event]
								new_score=saved_score+event_company_score
								possible_future_events_SCORE[possible_future_events_SCORE_event]=new_score

		## for each possible event, calculate score based on travelling time ##
		for possible_future_events_event in possible_future_events:
			possible_event_location=venues_events[possible_future_events_event].strip(' \n')
			possible_event_coords=venues_coords[possible_event_location]
			orig_coord=current_loc_coords
			dest_coord=possible_event_coords
			#calculate travelling time and assign score base on walking time
			url_walking = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=walking&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
			result_walking= simplejson.load(urllib.urlopen(url_walking))
			walking_time = result_walking['rows'][0]['elements'][0]['duration']['value']
			mins_walking_time=round(walking_time/60,1)
			#<=5 mins:3   <=10mins:2 >10mins:1
			if mins_walking_time<=2.5:
				temp_score=travellingtime_weightage*3
				for possible_future_events_SCORE_event in possible_future_events_SCORE:
					if possible_future_events_event==possible_future_events_SCORE_event:
							saved_score=possible_future_events_SCORE[possible_future_events_SCORE_event]
							new_score=saved_score+temp_score
							possible_future_events_SCORE[possible_future_events_SCORE_event]=new_score
			elif mins_walking_time<=10.0:
				temp_score=travellingtime_weightage*2
				for possible_future_events_SCORE_event in possible_future_events_SCORE:
					if possible_future_events_event==possible_future_events_SCORE_event:
							saved_score=possible_future_events_SCORE[possible_future_events_SCORE_event]
							new_score=saved_score+temp_score
							possible_future_events_SCORE[possible_future_events_SCORE_event]=new_score
			else:
				temp_score=travellingtime_weightage*1
				for possible_future_events_SCORE_event in possible_future_events_SCORE:
					if possible_future_events_event==possible_future_events_SCORE_event:
							saved_score=possible_future_events_SCORE[possible_future_events_SCORE_event]
							new_score=saved_score+temp_score
							possible_future_events_SCORE[possible_future_events_SCORE_event]=new_score


		## FINALIZE EVENTS ##
		highest_score_key=max(possible_future_events_SCORE, key=possible_future_events_SCORE.get)
		highest_score_value=possible_future_events_SCORE[highest_score_key]
		for event in possible_future_events_SCORE:
			if possible_future_events_SCORE[event]==highest_score_value:
				possible_future_events_final.append(event)

	else:
		#there are no recommended events for the user based on algorithm
		message="FAILURE"

	#what to display after submit button is clicked	
	return {'message':message, 'next_events':possible_future_events_final} 
