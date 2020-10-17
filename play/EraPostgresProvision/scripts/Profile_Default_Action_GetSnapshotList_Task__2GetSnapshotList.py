# Set creds and headers
era_user = '@@{era_creds.username}@@'
era_pass = '@@{era_creds.secret}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Time Machine Capability
url  = "https://@@{era_ip}@@:8443/era/v0.8/tms/@@{TM_ID}@@/capability?summary=false&time-zone=UTC"
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)

if resp.ok:
  
  # Cycle through the snapshot modes
  for modes in json.loads(resp.content)['capability']:
    print "{0} MODE".format(modes['mode'])
    
    # Cycle through the snapshots if they exist
    if modes['snapshots']:
      for snapshot in modes['snapshots']:
        print "  ------------------------"
        print "  Snapshot ID (copy this): {0}".format(snapshot['id'])
        print "  Snapshot Time Stamp:     {0}".format(snapshot['snapshotTimeStamp'])
        
    # Print message if the don't exist
    else:
      print "  ------------------------"
      print "  No {0} snapshots exist.".format(modes['mode'].lower())

else:
  print "Get Time Machine Capability request failed", json.dumps(json.loads(resp.content), indent=4)
  exit(1)