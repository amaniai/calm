# Set creds and headers
era_user = '@@{era_creds.username}@@'
era_pass = '@@{era_creds.secret}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Set the URL and payload
url     = "https://@@{era_ip}@@:8443/era/v0.8/tms/@@{TM_ID}@@/snapshots"
payload = {
  "actionHeader": [
    {
      "name": "snapshotName",
      "value": "@@{DB_NAME}@@_snap_@@{calm_time("%Y%m%d%H%M")}@@"
    }
  ]
}

# Make the call and set the response operation ID to the variable
resp = urlreq(url, verb='POST', auth='BASIC', user=era_user, passwd=era_pass, params=json.dumps(payload), headers=headers)
if resp.ok:
  print "SNAP_OPERATION_ID={0}".format(json.loads(resp.content)['operationId'])
else:
  print "Post Database create request failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)