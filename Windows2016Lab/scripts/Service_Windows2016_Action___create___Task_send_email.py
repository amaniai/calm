import requests

subject = 'Your access to @@{calm_application_name}@@ is ready ...'
email = '@@{EMAIL}@@'
message = '''

Dear user[@@{calm_int(calm_array_index) + 1}@@],

@@{calm_username}@@ provisioned an application for you.

To access your instance, you can login using the following credentials and URL:

URL: @@{PUBLIC_ACCESS_URL}@@
username: @@{ACCESS_USERNAME}@@
password: @@{ACCESS_PASSWORD}@@

note: username and password are case-sensitive

The local admin account for your Windows machine:
username: administrator
password: @@{ADMIN_PASS}@@


Thank you

'''


url = '@@{MAIL_GW}@@'
payload = {
  'to': email,
  'subject': subject,
  'body': message
}
resp = requests.post(url, json=payload)
if resp.status_code == 200:
  print('INFO - message sent to {}'.format(email))
else:
  print('ERROR - message failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
  exit(1)



