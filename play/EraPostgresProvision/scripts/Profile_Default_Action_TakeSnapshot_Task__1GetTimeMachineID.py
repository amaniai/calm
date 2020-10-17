# Set creds and headers
era_user = '@@{era_creds.username}@@'
era_pass = '@@{era_creds.secret}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Time Machine ID
url  = "https://@@{era_ip}@@:8443/era/v0.8/tms/name/@@{DB_NAME}@@_tm?load-drive=false"
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if resp.ok:
  print "TM_ID={0}".format(json.loads(resp.content)['id'])
else:
  print "Get Time Machine ID request failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)