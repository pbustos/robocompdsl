#!/usr/bin/env python
# -*- coding: utf-8 -*-
[[[cog

import sys
sys.path.append('/opt/robocomp/python')

import cog
def A():
	cog.out('<@@<')
def Z():
	cog.out('>@@>')
def TAB():
	cog.out('<TABHERE>')

from parseCDSL import *
component = CDSLParsing.fromFile(theCDSL)

import specificworker

REQUIRE_STR = """
<TABHERE><TABHERE><TABHERE># Remote object connection for <NORMAL>
<TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE>proxyString = self.communicator().getProperties().getProperty('<NORMAL>Proxy')
<TABHERE><TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>basePrx = self.communicator().stringToProxy(proxyString)
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>self.<LOWER>_proxy = RoboComp<NORMAL>.<NORMAL>Prx.checkedCast(basePrx)
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>mprx["<NORMAL>Proxy"] = self.<LOWER>_proxy
<TABHERE><TABHERE><TABHERE><TABHERE>except:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>print 'Cannot connect to the remote object.'
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>return
<TABHERE><TABHERE><TABHERE>except Ice.Exception, e:
<TABHERE><TABHERE><TABHERE><TABHERE>print e
<TABHERE><TABHERE><TABHERE><TABHERE>print 'Cannot get <NORMAL>Proxy property.'
<TABHERE><TABHERE><TABHERE><TABHERE>return
"""

SUBSCRIBESTO_STR = """
<TABHERE><TABHERE><TABHERE># Server adapter creation and publication
<TABHERE><TABHERE><TABHERE>proxy = self.communicator().getProperties().getProperty( "TopicManager.Proxy")
<TABHERE><TABHERE><TABHERE>print proxy
<TABHERE><TABHERE><TABHERE>topicManager = IceStorm.TopicManagerPrx.checkedCast(self.communicator().stringToProxy(proxy))
<TABHERE><TABHERE><TABHERE>print topicManager

<TABHERE><TABHERE><TABHERE><NORMAL>_adapter = self.communicator().createObjectAdapter("<NORMAL>Topic")
<TABHERE><TABHERE><TABHERE><LOWER>I_ = <NORMAL>I(handler, self.communicator)
<TABHERE><TABHERE><TABHERE><LOWER>_proxy = <NORMAL>_adapter.addWithUUID(<LOWER>I_).ice_oneway()

<TABHERE><TABHERE><TABHERE>subscribeDone = False
<TABHERE><TABHERE><TABHERE>while not subscribeDone:
<TABHERE><TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><LOWER>_topic = topicManager.create("<NORMAL>")
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>subscribeDone = True
<TABHERE><TABHERE><TABHERE><TABHERE>except:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><LOWER>_topic = topicManager.retrieve("<NORMAL>")
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>subscribeDone = True
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>except e:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>print e
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>print "Error. Topic does not exist"
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>sys.exit(-1)
<TABHERE><TABHERE><TABHERE>qos = {}
<TABHERE><TABHERE><TABHERE><LOWER>_topic.subscribeAndGetPublisher(qos, <LOWER>_proxy)
<TABHERE><TABHERE><TABHERE><NORMAL>_adapter.activate()
"""

PUBLISHES_STR = """
<TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE>topic = False
<TABHERE><TABHERE><TABHERE><TABHERE>topic = topicManager.retrieve("<NORMAL>")
<TABHERE><TABHERE><TABHERE>except:
<TABHERE><TABHERE><TABHERE><TABHERE>pass
<TABHERE><TABHERE><TABHERE>while not topic:
<TABHERE><TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>topic = topicManager.retrieve("AprilTagsTopic")
<TABHERE><TABHERE><TABHERE><TABHERE>except IceStorm.NoSuchTopic:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>topic = topicManager.create("<NORMAL>")
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>except:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>print 'Another client created the <NORMAL> topic... ok'
<TABHERE><TABHERE><TABHERE>pub = topic.getPublisher().ice_oneway()
<TABHERE><TABHERE><TABHERE>executiveTopic = RoboCompAGMExecutive.AGMExecutiveTopicPrx.uncheckedCast(pub)


<TABHERE>IceStorm::TopicPrx <LOWER>_topic;
<TABHERE>while (!<LOWER>_topic)
<TABHERE>{
<TABHERE><TABHERE>try
<TABHERE><TABHERE>{
<TABHERE><TABHERE><TABHERE><LOWER>_topic = topicManager->retrieve("<NORMAL>");
<TABHERE><TABHERE>}
<TABHERE><TABHERE>catch (const IceStorm::NoSuchTopic&)
<TABHERE><TABHERE>{
<TABHERE><TABHERE><TABHERE>try
<TABHERE><TABHERE><TABHERE>{
<TABHERE><TABHERE><TABHERE><TABHERE><LOWER>_topic = topicManager->create("<NORMAL>");
<TABHERE><TABHERE><TABHERE>}
<TABHERE><TABHERE><TABHERE>catch (const IceStorm::TopicExists&){
<TABHERE><TABHERE><TABHERE><TABHERE>// Another client created the topic.
<TABHERE><TABHERE><TABHERE>}
<TABHERE><TABHERE>}
<TABHERE>}
<TABHERE>Ice::ObjectPrx <LOWER>_pub = <LOWER>_topic->getPublisher()->ice_oneway();
<TABHERE><NORMAL>Prx <LOWER> = <NORMAL>Prx::uncheckedCast(<LOWER>_pub);
<TABHERE>mprx["<NORMAL>Pub"] = (::IceProxy::Ice::Object*)(&<LOWER>);
"""

IMPLEMENTS_STR = """
<TABHERE><TABHERE><TABHERE>handler = <NORMAL>I()
<TABHERE><TABHERE><TABHERE>handler.start()
<TABHERE><TABHERE><TABHERE>adapter = self.communicator().createObjectAdapter('<NORMAL>Comp')
<TABHERE><TABHERE><TABHERE>adapter.add(<NORMAL>I(handler), self.communicator().stringToIdentity('<LOWER>'))
#<TABHERE><TABHERE><TABHERE>adapter.add(CommonBehaviorI(handler, self.communicator), self.communicator().stringToIdentity('commonbehavior'))
<TABHERE><TABHERE><TABHERE>adapter.activate()

<TABHERE><TABHERE>// Server adapter creation and publication
<TABHERE><TABHERE>Ice::ObjectAdapterPtr adapter<NORMAL> = communicator()->createObjectAdapter("<NORMAL>Comp");
<TABHERE><TABHERE><NORMAL>I *<LOWER> = new <NORMAL>I(worker);
<TABHERE><TABHERE>adapter<NORMAL>->add(<LOWER>, communicator()->stringToIdentity("<LOWER>"));
"""
]]]
[[[end]]]

#    Copyright (C)
[[[cog
A()
import datetime
cog.out(str(datetime.date.today().year))
Z()
]]]
[[[end]]]
 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

# \mainpage RoboComp::
[[[cog
A()
cog.out(component['name'])
]]]
[[[end]]]
#
# \section intro_sec Introduction
#
# Some information about the component...
#
# \section interface_sec Interface
#
# Descroption of the interface provided...
#
# \section install_sec Installation
#
# \subsection install1_ssec Software depencences
# Software dependences....
#
# \subsection install2_ssec Compile and install
# How to compile/install the component...
#
# \section guide_sec User guide
#
# \subsection config_ssec Configuration file
#
# <p>
# The configuration file...
# </p>
#
# \subsection execution_ssec Execution
#
# Just: "${PATH_TO_BINARY}/
[[[cog
A()
cog.out(component['name'])
Z()
]]]
[[[end]]]
 --Ice.Config=${PATH_TO_CONFIG_FILE}"
#
# \subsection running_ssec Once running
#
#
#

import sys, traceback, Ice, IceStorm, subprocess, threading, time, Queue, os

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	pass
if len(ROBOCOMP)<1:
	print 'ROBOCOMP environment variable not set! Exiting.'
	sys.exit()


preStr = "-I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/"
Ice.loadSlice(preStr+"CommonBehavior.ice")
import RoboCompCommonBehavior
[[[cog
for imp in component['imports']:
	print (imp)
	module = IDSLParsing.gimmeIDSL(imp.split('/')[-1])
	incl = imp.split('/')[-1].split('.')[0]
	cog.outl('Ice.loadSlice(preStr+"'+incl+'.ice")')
	cog.outl('import '+module['name']+'')
]]]
[[[end]]]


class CommonBehaviorI (RoboCompCommonBehavior.CommonBehavior):
	def __init__(self, _handler, _communicator):
		self.handler = _handler
		self.communicator = _communicator
	def getFreq(self, current = None):
		self.handler.getFreq()
	def setFreq(self, freq, current = None):
		self.handler.setFreq()
	def timeAwake(self, current = None):
		try:
			return self.handler.timeAwake()
		except:
			print 'Problem getting timeAwake'
	def killYourSelf(self, current = None):
		self.handler.killYourSelf()
	def getAttrList(self, current = None):
		try:
			return self.handler.getAttrList(self.communicator)
		except:
			print 'Problem getting getAttrList'
			traceback.print_exc()
			status = 1
			return



class MainClass (Ice.Application):
	def run (self, argv):
		status = 0
		mprx = {}
		try:
			self.shutdownOnInterrupt()

[[[cog
for rq in component['requires']:
	w = REQUIRE_STR.replace("<NORMAL>", rq).replace("<LOWER>", rq.lower())
	cog.outl(w)
]]]
[[[end]]]

[[[cog
try:
	if len(component['publishes']) > 0 or len(component['subscribes']) > 0:
		cog.outl("""
<TABHERE><TABHERE># Topic Manager
<TABHERE><TABHERE>proxy = self.communicator().getProperties().getProperty("TopicManager.Proxy")
<TABHERE><TABHERE>obj = self.communicator().stringToProxy(proxy)
<TABHERE><TABHERE>topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)""")
except:
	pass
]]]
[[[end]]]


[[[cog
for pb in component['publishes']:
	w = PUBLISHES_STR.replace("<NORMAL>", pb).replace("<LOWER>", pb.lower())
	cog.outl(w)
]]]
[[[end]]]


			worker = SpecificWorker(mprx);
			connect(worker, SIGNAL(kill()), a, SLOT(quit()));

			self.communicator().waitForShutdown()
		except:
			traceback.print_exc()
			status = 1

		if self.communicator():
			try:
				self.communicator().destroy()
			except:
				traceback.print_exc()
				status = 1

MainClass( ).main(sys.argv)
