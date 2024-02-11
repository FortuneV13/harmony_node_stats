# VStats TOKEN
VSTATS_API = "https://vstats.fortune-validator.pro/api/node-stats"
VSTATS_TOKEN=""

#Shard Data 
NODE_ARRAY = [
    {
        "unique_name": "S0", # Keep it short | Used in node_stats summaries to identify node | Must be unique
        "shard":0, # Fall back to send to vstats if metadata fails to load . i.e service not running
        "service_name":"harmony", # Default is harmony
        "harmony_folder":"/home/serviceharmony/harmony", # Path to your harmony binary dir
        "http_port":9500, # Default is 9500
    }
]