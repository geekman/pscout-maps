#!/usr/bin/env python
#
# Parses PScout mappings at http://pscout.csl.toronto.edu/
# 2014.07.24 darell tan
#

import os
import sys
import re

METHOD_RE = re.compile(r'(\S+)\s+([a-z0-9_<>]+)\s*\(([^)]*)\)', re.IGNORECASE)

def transform_signature(line):
	"""Turns each line into a (klass, (return_type, method_name, args1, .. argN)) tuple"""
	line = line.strip('<>')
	klass, method = line.split(':', 1)
	klass = klass.strip()
	method = method.strip()

	method_match = METHOD_RE.match(method)
	method_parts = tuple([method_match.group(i) for i in range(1, 4)])

	return klass, method_parts

def class2type(klass):
	"""Transforms fully-qualified dotted class name to Java type representation."""
	return 'L' + klass.replace('.', '/') + ';'

def main():
	methods = []

	for fname in sys.argv[1:]:
		f = open(fname, 'rb')
		for line in f:
			line = line.strip()
			if line[0] == '<' and line[-1] == '>':
				methods.append(transform_signature(line))
		f.close()

	# remove duplicates
	methods = set(methods)

	# unique classes
	classes = set(c for c, _ in methods)

	# all classes & methods
	#for klass, method in methods:
	#	print klass, method[1]

	for c in classes:
		print class2type(c)

if __name__ == '__main__':
	main()

