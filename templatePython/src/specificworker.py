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
if component == None:
	print('Can\'t locate', theCDSLs)
	sys.exit(1)

from parseIDSL import *
pool = IDSLPool(theIDSLs)


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

from PySide import *
from genericworker import *

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map, parent):

		print 'SpecificWorker.__init__ A'
		super(SpecificWorker, self).__init__(proxy_map)

		print 'SpecificWorker.__init__ N'
		self.timer.timeout.connect(self.compute)
		self.timer.start(self.Period)

		print 'SpecificWorker.__init__ Z'

	def setParams(self, params):
		#// 	try
		#// 	{
		#// 		RoboCompCommonBehavior::Parameter par = params.at("InnerModelPath");
		#// 		innermodel_path=par.value;
		#// 		innermodel = new InnerModel(innermodel_path);
		#// 	}
		#// 	catch(std::exception e) { qFatal("Error reading config params"); }
		return True

	@QtCore.Slot()
	def compute(self):
		print 'SpecificWorker.compute...'
		#// 	try
		#// 	{
		#// 		camera_proxy->getYImage(0,img, cState, bState);
		#// 		memcpy(image_gray.data, &img[0], m_width*m_height*sizeof(uchar));
		#// 		searchTags(image_gray);
		#// 	}
		#// 	catch(const Ice::Exception &e)
		#// 	{
		#// 		std::cout << "Error reading from Camera" << e << std::endl;
		#// 	}
		return True

[[[cog
if 'implements' in component:
	for imp in component['implements']:
		module = pool.moduleProviding(imp)
		for interface in module['interfaces']:
			if interface['name'] == imp:
				for mname in interface['methods']:
					method = interface['methods'][mname]
					paramStrA = ''
					for p in method['params']:
						if paramStrA == '': delim = ''
						else: delim = ', '
						if p['decorator'] == 'out':
							const = ''
						else:
							const = 'const '
						if  p['type'] in [ 'int' ]:
							ampersand = ''
						else:
							ampersand = '&'
						paramStrA += const + p['type'] + ' ' + ampersand + p['name'] + delim
					cog.outl('<TABHERE>def ' + method['name'] + '(self, ' + paramStrA + "):\n<TABHERE>pass\n")
]]]
[[[end]]]

[[[cog
if 'subscribesTo' in component:
	for sub in component['subscribesTo']:
		module = pool.moduleProviding(sub)
		for interface in module['interfaces']:
			if interface['name'] == sub:
				for mname in interface['methods']:
					method = interface['methods'][mname]
					paramStrA = ''
					for p in method['params']:
						if paramStrA == '': delim = ''
						else: delim = ', '
						if p['decorator'] == 'out':
							const = ''
						else:
							const = 'const '
						if  p['type'] in [ 'int' ]:
							ampersand = ''
						else:
							ampersand = '&'
						paramStrA += const + p['type'] + ' ' + ampersand + p['name'] + delim
					cog.outl('<TABHERE>def ' + method['name'] + '(self, ' + paramStrA + "):\n<TABHERE>pass\n")
]]]
[[[end]]]


