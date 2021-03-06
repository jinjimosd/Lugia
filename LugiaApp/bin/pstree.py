#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2011-2015 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

#Ps tree logic copied from Giampaolo Rodola's gitub
# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#https://github.com/giampaolo
#https://github.com/giampaolo/psutil/blob/master/scripts/pstree.py



from __future__ import absolute_import, division, print_function, unicode_literals
from splunklib.searchcommands import dispatch, EventingCommand, Configuration, Option, validators
import sys
import collections

@Configuration()
class PSTreeCommand(EventingCommand):
	""" Displays a tree structure using a parent and child field from splunk logs. Intended for sysmon EventCode=1 events 
	but can be used for anything. App will return a multivalue field for each root process displaying all children 
	processes in tree format.
	##Syntax
	.. code-block::
	pstree parent=<field> child=<field> 
	##Description
	Returns a tree structure of the parent and child fields. Childern will be indented for each  Each  Logs must be received in chronological order 
	for accurate results. 
	##Example
	Count the number of words in the `text` of each tweet in tweets.csv and store the result in `word_count`.
	.. code-block::
	index=sysmon EventCode=1 | pstree parent=ParentProcessID child=ProcessID
	"""

	parent = Option(
	doc='''
	**Syntax:** **parent=***<fieldname>*
	**Description:** Name of the field that holds the parent value''',
	require=True, validate=validators.Fieldname())

	child = Option(
	doc='''
	**Syntax:** **child=***<fieldname>*
	**Description:** Name of the field that holds the child value''',
	require=True, validate=validators.Fieldname())

	def make_tree(self,parent, tree, indent, return_array, prefix):
		return_array.append(prefix+parent)
		if parent not in tree:
			return 
		children = tree[parent]#[:-1]
		for child in children:
			self.make_tree(child, tree, indent + "`` ",return_array, indent + "|--- ")
		#child = tree[parent][-1]
		#self.make_tree(child, tree, indent + "  ",return_array, indent + "\_ ")
		

	def transform(self, records):
		self.logger.debug('PSTreeCommandCommand: %s', self)  # logs command line
		tree= collections.defaultdict(list)
		children=[]
		for record in records:
			tree[record[self.parent]].append(record[self.child])
			children.append(record[self.child])
		for parent in tree:
			if parent not in children:
				tmp=[]
				self.make_tree(parent,tree,'',tmp,'')
				yield {"tree":tmp}

dispatch(PSTreeCommand, sys.argv, sys.stdin, sys.stdout, __name__)
