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
#- Comment out http_port if NOT running a multiple shard server
SHARD_ARRAY = {
	 
	# "shard-0":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"node_port":"" #optional - only if running multi shard server
	# },
	
	"shard-1":{
		"harmony_folder":"/home/serviceharmony/harmony",
		"http_port":"" #optional - only if running multi shard server
	},
	
	# "shard-2":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":"" #optional - only if running multi shard server
	# },
	
    # "shard-3":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":"" #optional - only if running multi shard server
	# },
	
}

