
from .auth import get_auth

from mastodon import Mastodon


def main(url, email=None, auth_file="~/.mastotext-auth.json"):
	client_id, secret, access_token = get_auth(auth_file, url, email)

	# testing code
	from pprint import pprint
	print "Got creds."
	api = Mastodon(
		api_base_url=url,
		client_id=client_id,
		client_secret=secret,
		access_token=access_token,
	)
	print "Verifying we're logged in"
	pprint(api.account_verify_credentials())
	print "Fetching latest 10 toots"
	pprint(api.timeline_home(limit=10))
	print "Done."
