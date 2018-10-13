#!/usr/bin/env python3.6
# encoding: utf-8

import re
from setuptools import setup


with open('ben_cogs/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('requirements.txt') as f:
	dependency_links = [line for line in f if line and not line.lstrip().startswith('#')]

setup(
	name='ben_cogs',
	author='bmintz',
	author_email='bmintz@protonmail.com',
	url='https://github.com/bmintz/cogs',
	download_url='https://github.com/bmintz/cogs/archive/{}.tar.gz'.format(version),
	version=version,
	packages=['ben_cogs'],
	dependency_links=dependency_links,
	install_requires=[
		'discord.py>=1.0.0a1430',
		'humanize',
		'import_expression<1.0.0',
		'jishaku',
		'objgraph',
		'psutil'],
	python_requires='>=3.6.0',
	license='MIT',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Framework :: AsyncIO',
		'License :: OSI Approved :: MIT License',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.6',
		'Topic :: Internet',
		'Topic :: Utilities'])
