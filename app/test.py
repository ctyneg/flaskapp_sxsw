import simplejson, urllib
	
orig_coord = 30.265494, -97.747213
dest_coord = 30.270295, - 97.734118
url_driving = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
result_driving= simplejson.load(urllib.urlopen(url_driving))
driving_time = result_driving['rows'][0]['elements'][0]['duration']['value']
url_walking = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=walking&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
result_walking= simplejson.load(urllib.urlopen(url_walking))
walking_time = result_walking['rows'][0]['elements'][0]['duration']['value']
url_bicycling = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=bicycling&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
result_bicycling= simplejson.load(urllib.urlopen(url_bicycling))
bicycling_time = result_bicycling['rows'][0]['elements'][0]['duration']['value']

print "driving time " + str(driving_time) +"s"
print "walking time " + str(walking_time) +"s"
print "bicycling time " + str(bicycling_time) +"s"