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
#- Change http_port if running a multiple shard server #9501 is the default harmony.conf port under HTTP
SHARD_ARRAY = {
	 
	"first-shard":{
		"harmony_folder":"/home/serviceharmony/harmony",
		"node_port":9501 
	},
	 
	# "second-shard":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501 
	# },
	
	# "third-shard":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501 
	# },
	
    # "forth-shard":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501 
	# },
	
}

