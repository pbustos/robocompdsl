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


REQUIRE_STR = """
<TABHERE>try
<TABHERE>{
<TABHERE><TABHERE><LOWER>_proxy = <NORMAL>Prx::uncheckedCast( communicator()->stringToProxy( getProxyString("<NORMAL>Proxy") ) );
<TABHERE>}
<TABHERE>catch(const Ice::Exception& ex)
<TABHERE>{
<TABHERE><TABHERE>cout << "[" << PROGRAM_NAME << "]: Exception: " << ex;
<TABHERE><TABHERE>return EXIT_FAILURE;
<TABHERE>}
<TABHERE>rInfo("<NORMAL>Proxy initialized Ok!");
<TABHERE>mprx["<NORMAL>Proxy"] = (::IceProxy::Ice::Object*)(&<LOWER>_proxy);//Remote server proxy creation example
"""

SUBSCRIBESTO_STR = """
<TABHERE><TABHERE>// Server adapter creation and publication
<TABHERE><TABHERE>Ice::ObjectAdapterPtr <NORMAL>_adapter = communicator()->createObjectAdapter("<NORMAL>Topic");
<TABHERE><TABHERE><NORMAL>Ptr <LOWER>I_ = new <NORMAL>I(worker);
<TABHERE><TABHERE>Ice::ObjectPrx <LOWER>_proxy = <NORMAL>_adapter->addWithUUID(<LOWER>I_)->ice_oneway();
<TABHERE><TABHERE>IceStorm::TopicPrx <LOWER>_topic;
<TABHERE><TABHERE>if(!<LOWER>_topic){
<TABHERE><TABHERE>try {
<TABHERE><TABHERE><TABHERE><LOWER>_topic = topicManager->create("<NORMAL>");
<TABHERE><TABHERE>}
<TABHERE><TABHERE>catch (const IceStorm::TopicExists&) {
<TABHERE><TABHERE>//Another client created the topic
<TABHERE><TABHERE>try{
<TABHERE><TABHERE><TABHERE><LOWER>_topic = topicManager->retrieve("<NORMAL>");
<TABHERE><TABHERE>}
<TABHERE><TABHERE>catch(const IceStorm::NoSuchTopic&)
<TABHERE><TABHERE>{
<TABHERE><TABHERE><TABHERE>//Error. Topic does not exist
<TABHERE><TABHERE><TABHERE>}
<TABHERE><TABHERE>}
<TABHERE><TABHERE>IceStorm::QoS qos;
<TABHERE><TABHERE><LOWER>_topic->subscribeAndGetPublisher(qos, <LOWER>_proxy);
<TABHERE><TABHERE>}
<TABHERE><TABHERE><NORMAL>_adapter->activate();
"""

PUBLISHES_STR = """
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
<TABHERE><TABHERE>// Server adapter creation and publication
<TABHERE><TABHERE>Ice::ObjectAdapterPtr adapter<NORMAL> = communicator()->createObjectAdapter("<NORMAL>Comp");
<TABHERE><TABHERE><NORMAL>I *<LOWER> = new <NORMAL>I(worker);
<TABHERE><TABHERE>adapter<NORMAL>->add(<LOWER>, communicator()->stringToIdentity("<LOWER>"));
"""
]]]
[[[end]]]

#    Copyright (C) 2010 by 
[[[cog
A()
import datetime
cog.out(str(datetime.date.today().year))
]]]
[[[end]]]
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

import sys, traceback, Ice, subprocess, threading, time, Queue, os

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	pass
if len(ROBOCOMP)<1:
	print 'ROBOCOMP environment variable not set! Exiting.'
	sys.exit()


[[[cog
A()
for imp in component['imports']:
	print (imp)
	module = IDSLParsing.gimmeIDSL(imp.split('/')[-1])
	incl = imp.split('/')[-1].split('.')[0]
	cog.outl('Ice.loadSlice(ROBOCOMP+"/interfaces/'+incl+'.ice")')
	cog.outl('import '+module['name']+'')
Z()
]]]
[[[end]]]


import RoboCompSpeech
import RoboCompAprilTags
import RoboCompCommonBehavior

import IceStorm


sleep_time = 0.1
max_queue = 100
charsToAvoid = ["'", '"', '{', '}', '[', '<', '>', '(', ')', '&', '$', '|', '#']

class SpeechHandler (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.text_queue = Queue.Queue(max_queue)
		self.accessLock = threading.Lock()
		self.initTime = time.time()
	def run (self):
		while 1:
			self.accessLock.acquire()
			if self.text_queue.empty():
				self.accessLock.release()
				time.sleep(sleep_time)
			else:
				text_to_say = self.text_queue.get()
				self.accessLock.release()
				for rep in charsToAvoid:
					text_to_say = text_to_say.replace(rep, '\\'+rep)
				shellcommand = "echo " + text_to_say  + " | padsp festival --tts"
				print 'Order: ' + text_to_say
				print 'Shell: "' + shellcommand + '"'
				os.system(shellcommand)
	def put (self, new_text, force):
		self.accessLock.acquire()
		if force:
			os.system("killall -9 festival")
			os.system("killall -9 aplay")
			self.text_queue = Queue.Queue(max_queue)
		self.text_queue.put(new_text)
		self.accessLock.release()

	def getFreq(self):
		return 5

	def setFreq(self, freq):
		print "Setting freq of acpi"

	def timeAwake(self):
		timeA=int(time.time()-self.initTime)
		type(timeA)
		return timeA


	def killYourSelf(self):
		print "Killing acpi component"

	def getAttrList(self, communicator):
		#~ attrList = dict()
		print "Obteniendo property dict"
		propertydict=communicator().getProperties().getPropertiesForPrefix("")
		print len(propertydict)
		attrList= []
		for k, v in propertydict.iteritems():
			attr= RoboCompCommonBehavior.AttrPair()
			attr.name=k
			attr.value=v
			attrList.append(attr)
		return attrList

class SpeechI (RoboCompSpeech.Speech):
	def __init__(self,_handler):
		self.handler = _handler
	def say(self, text, force, current=None):
		print text
		try:
			self.handler.put(text, force)
		except:
			print 'Full queue.'
	def isBusy(self, current=None):
		return 'festival' in subprocess.Popen(["ps", "ax"], stdout=subprocess.PIPE).communicate()[0]

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


class AprilTagsI (RoboCompAprilTags.AprilTags):
	def __init__(self, _handler, _communicator):
		self.handler = _handler
		self.communicator = _communicator
	def newAprilTag(self, tags, current = None):
		print 't'


class Server (Ice.Application):
	def run (self, argv):
		status = 0
		try:
			self.shutdownOnInterrupt()


			# Proxy to publish AGMExecutiveTopic
			proxy = self.communicator().getProperties().getProperty("TopicManager.Proxy")
			obj = self.communicator().stringToProxy(proxy)
			topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
			try:
				topic = False
				topic = topicManager.retrieve("AprilTagsTopic")
			except:
				pass
			while not topic:
				try:
					topic = topicManager.retrieve("AprilTagsTopic")
				except IceStorm.NoSuchTopic:
					try:
						topic = topicManager.create("AprilTagsTopic")
					except:
						print 'Another client created the AprilTagsTopic topic... ok'
			pub = topic.getPublisher().ice_oneway()
			executiveTopic = RoboCompAGMExecutive.AGMExecutiveTopicPrx.uncheckedCast(pub)



			handler= SpeechHandler()
			handler.start()
			adapter = self.communicator().createObjectAdapter('SpeechComp')
			adapter.add(SpeechI(handler), self.communicator().stringToIdentity('speech'))
			adapter.add(CommonBehaviorI(handler, self.communicator), self.communicator().stringToIdentity('commonbehavior'))
			adapter.activate()


			# Server adapter creation and publication
			proxy = self.communicator().getProperties().getProperty( "TopicManager.Proxy")
			print proxy
			topicManager = IceStorm.TopicManagerPrx.checkedCast(self.communicator().stringToProxy(proxy))
			print topicManager

			AprilTags_adapter = self.communicator().createObjectAdapter("AprilTagsTopic")
			apriltagsI_ = AprilTagsI(handler, self.communicator)
			apriltags_proxy = AprilTags_adapter.addWithUUID(apriltagsI_).ice_oneway()

			subscribeDone = False
			while not subscribeDone:
				try:
					apriltags_topic = topicManager.create("AprilTags")
					subscribeDone = True
				except:
					try:
						apriltags_topic = topicManager.retrieve("AprilTags")
						subscribeDone = True
					except e:
						print e
						print "Error. Topic does not exist"
						sys.exit(-1)
			qos = {}
			apriltags_topic.subscribeAndGetPublisher(qos, apriltags_proxy)
			AprilTags_adapter.activate()
			print 'hecho'


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

Server( ).main(sys.argv)
