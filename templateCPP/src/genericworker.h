/*
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
 *    Copyright (C) 
[[[cog
A()
import datetime
cog.out(str(datetime.date.today().year))
Z()
]]]
[[[end]]]
 by YOUR NAME HERE
 *
 *    This file is part of RoboComp
 *
 *    RoboComp is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    RoboComp is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef GENERICWORKER_H
#define GENERICWORKER_H

#include "config.h"
#include <QtGui>
#include <stdint.h>
#include <qlog/qlog.h>

#include <CommonBehavior.h>
[[[cog

for m in pool.modulePool:
	cog.outl("#include <"+m+".h>")

]]]
[[[end]]]


#define CHECK_PERIOD 5000
#define BASIC_PERIOD 100

typedef map <string,::IceProxy::Ice::Object*> MapPrx;

using namespace std;

[[[cog

pool = IDSLPool(theIDSLs)
for m in pool.modulePool:
	cog.outl("using namespace "+pool.modulePool[m]['name']+";")

]]]
[[[end]]]

class GenericWorker : public QObject
{
Q_OBJECT
public:
	GenericWorker(MapPrx& mprx, QObject *parent = 0);
	virtual ~GenericWorker();
	virtual void killYourSelf();
	virtual void setPeriod(int p);
	
	virtual bool setParams(RoboCompCommonBehavior::ParameterList params) = 0;
	QMutex *mutex;

[[[cog
for req in component['requires']:
	cog.outl("<TABHERE>"+req+"Prx " + req.lower() + "_proxy;")
]]]
[[[end]]]


[[[cog
for pub in component['publishes']:
	cog.outl("<TABHERE>"+pub+" "    + pub.lower() + ";")
]]]
[[[end]]]


[[[cog
if 'implements' in component:
	for imp in component['implements']:
		for interface in module['interfaces']:
			if interface['name'] == imp:
				for mname in interface['methods']:
					method = interface['methods'][mname]
						cog.outl("virtual IMPLEMENTS " + method)
]]]
[[[end]]]


[[[cog
if 'subscribes' in component:
	for sub in component['subscribes']:
		cog.outl("SUBSCRIBES " + sub)
]]]
[[[end]]]


	virtual listaMarcas checkMarcas() = 0;

protected:
	QTimer timer;
	int Period;
public slots:
	virtual void compute() = 0;
signals:
	void kill();
};

#endif