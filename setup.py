from setuptools import setup, find_packages

setup(
	name='mastotext',
	version='0.0.1',
	author='Mike Lang',
	author_email='mikelang3000@gmail.com',
	description='Terminal-based Mastodon client app',
	packages=find_packages(),
	install_requires=[
		"argh",
		"mastodon.py",
	],
)
