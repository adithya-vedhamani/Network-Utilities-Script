# Network Utilties

## nslookup.py

### Overview
This is a Flask-based API for performing DNS lookups using the `nslookup` command. The API accepts HTTP GET requests with query parameters and returns the result of the nslookup command as a JSON response.

### Setup
1. Install Flask: `pip install Flask`
2. Run the script: `python nslookup.py`

### Usage
#### Perform NSLookup
Make a GET request to the `/nslookup` endpoint with the following query parameters:
- `query` (required): The domain or IP address to look up.
- `options` (optional): Comma-separated list of additional nslookup options.
- `server` (optional): The DNS server to use.

### Example
```bash
curl -X GET "http://127.0.0.1:5000/nslookup?query=example.com&options=-type=a"
```

### Response
The API will respond with a JSON object containing the result of the nslookup command.


## trace_route.py

### Overview
This is a Flask-based API for performing traceroute to multiple destinations concurrently using the scapy library. The API accepts HTTP POST requests with a JSON payload and returns the traceroute results for each destination.

### Setup
1. Install Flask: `pip install Flask`
2. Install Scapy: `pip install scapy`
3. Run the script: `python trace_route.py`

### Usage
#### Perform Traceroute
Make a POST request to the /traceroute endpoint with the following JSON payload:
```bash
{
  "destinations": ["example.com", "google.com"],
  "max_hops": 30,
  "timeout": 2
}
```


### Example:
```bash
curl -X POST -H "Content-Type: application/json" -d "@payload.json" http://127.0.0.1:5000/traceroute
```
### Response
The API will respond with a JSON object containing the traceroute results for each specified destination.

### Notes
The destinations parameter is required in the JSON payload.
max_hops and timeout are optional parameters, with default values of 30 and 2 seconds, respectively.
Traceroute is performed concurrently for each destination using threads.
