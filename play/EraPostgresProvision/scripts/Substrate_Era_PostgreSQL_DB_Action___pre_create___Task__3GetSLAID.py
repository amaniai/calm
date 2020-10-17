# Set creds and headers
era_user = '@@{era_creds.username}@@'
era_pass = '@@{era_creds.secret}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Set the db_name here, so we don't have the calm_time macro expanding at two different times
print "DB_NAME=@@{db_name_prefix}@@_{0}".format(@@{calm_time("%Y%m%d%H%M")}@@)

# Get the list of SLAs
url     = "https://@@{era_ip}@@:8443/era/v0.8/slas"
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)

# Find the desired SLA, and set the corresponding ID to the variable
if resp.ok:
  for sla in json.loads(resp.content):
    if sla['name'] == "@@{sla_name}@@":
      print "SLA_ID={0}".format(sla['id'])
else:
  print "Get SLA request failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)