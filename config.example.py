# vStatsBot Server Sync Token /token
VSTATS_API = "https://vstats.fortune-validator.pro/api/node-stats"

VSTATS_TOKEN=""

#Shard Data 
#- Comment/Uncomment as necessary 
#- Change http_port if running a multiple shard server #9500 is the default harmony.conf port under HTTP
SHARD_ARRAY = {
	"S0":{
		"harmony_folder":"/home/serviceharmony/harmony",
		"http_port":9500,
	},
	# "S1":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501,
	# },
}