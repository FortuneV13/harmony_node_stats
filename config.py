# vStatsBot Server Sync Token /token
VSTATS_TOKEN=""

# Validator Address
VALIDATOR_ADDRESS=""

# Double Signing Checks
DOUBLE_SIGN_CHECK_ENABLED=False

#Sync Check 
SYNC_CHECK_ENABLED=True

#Space Check
SPACE_CHECK_ENABLED=True




#Shard Data 
#- Comment/Uncomment as necessary 
#- Change http_port if running a multiple shard server
SHARD_ARRAY = {
	 
	# "shard-0":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"node_port":9501 
	# },
	 
	"shard-1":{
		"harmony_folder":"/home/serviceharmony/harmony",
		"http_port":9501 
	},
	
	# "shard-2":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501 
	# },
	
    # "shard-3":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501 
	# },
	
}

