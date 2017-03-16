# -*- coding: utf-8 -*-

import os

REPO_NAME = "michaelaeden.github.io"
DEBUG = True

# Assumes the app is in the same directory as this file
APP_DIR = os.path.dirname(os.path.abspath(__file__))

def parent_dir(path):
	"""Returns the parent folder of a directory"""
	return os.path.abspath(os.path.join(path, os.pardir))

PROJECT_ROOT = parent_dir(APP_DIR)
FREEZER_DESTINATION = PROJECT_ROOT
FREEZER_BASE_URL = "http://localhost/{0}".format(REPO_NAME)
FREEZER_REMOVE_EXTRA_FILES = False	# NOTE: if true, all app files are deleted when running freezer

FLATPAGES_MARKDOWN_EXTENSION = ['codehilite']
FLATPAGES_ROOT = os.path.join(APP_DIR, 'pages')
FLATPAGES_EXTENSION = '.md'