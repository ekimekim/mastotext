
import errno
import json
import os
import sys
from getpass import getpass

from mastodon import Mastodon


# These values are used to help explain to the server who we are.
CLIENT_NAME = 'mastotext'
WEBSITE = 'https://github.com/ekimekim/mastotext'


# Note: if you change the requested scopes, you'll need to remove the cache of client id/secrets.
# Format is {scope name: help text for why it's needed}
SCOPES = {
	'read': "Basic access, view timeline, etc",
}


def get_auth(auth_file, instance_url, email=None):
	"""Either retrieve (client id, secret) from auth file, or register new app."""
	auth_file = os.path.expanduser(auth_file)

	try:
		with open(auth_file) as f:
			auth_data = json.load(f)
	except EnvironmentError as e:
		if e.errno == errno.ENOENT:
			auth_data = {}
		else:
			raise e

	changed = False

	if instance_url in auth_data:
		info = auth_data[instance_url]
	else:
		client_id, secret = register_app(instance_url)
		info = {
			'client_id': client_id,
			'secret': secret,
			'access_tokens': {},
		}
		auth_data[instance_url] = info
		changed = True

	if email is None:
		if len(info['access_tokens']) == 1:
			email, = info['access_tokens'].keys()
		else:
			if info['access_tokens']:
				msg = (
					"Credentials for multiple users on this instance are saved.\n"
					"Available users:\n{}"
				).format('\n'.join('\t{}'.format(u for u in info['access_tokens'])))
			else:
				msg = "No existing credentials for any users on this instance."
			print msg
			print "Please re-run with --email set."
			sys.exit(1)

	if email not in info['access_tokens']:
		info['access_tokens'][email] = get_access_token(info, instance_url, email)
		changed = True

	if changed:
		output = json.dumps(auth_data)
		with open(auth_file, 'w') as f:
			f.write(output + '\n')

	return info['client_id'], info['secret'], info['access_tokens'][email]


def register_app(instance_url):
	return Mastodon.create_app(
		CLIENT_NAME,
		scopes=SCOPES,
		api_base_url=instance_url,
		website=WEBSITE,
	)


def get_access_token(client_auth, instance_url, email):
	password = getpass((
		"We need to authenticate with {url} to get permission to act on your behalf.\n"
		"We will register under the name {client!r} and request the following permissions:\n"
		"{scopes}\n"
		"We use your password to get an access token, which is saved and used for future authentication.\n"
		"Your password will not be saved.\n"
		"\n"
		"Password for {email} on instance {url}: "
	).format(
		url=instance_url,
		client=CLIENT_NAME,
		email=email,
		scopes='\n'.join('\t{}: {}'.format(scope, why) for scope, why in SCOPES.items()),
	))
	return Mastodon(
		api_base_url=instance_url,
		client_id=client_auth['client_id'],
		client_secret=client_auth['secret'],
	).log_in(email, password, scopes=SCOPES)
