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
def SPACE(i=0):
	s = ''
	if i>0:
		s = str(i)
	cog.out('<S'+s+'>')

from parseCDSL import *
component = CDSLParsing.fromFile(theCDSL)

]]]
[[[end]]]

cmake_minimum_required(VERSION 2.6)
PROJECT( 
[[[cog
A()
cog.out(' ' + component['name'])
Z()
]]]
[[[end]]]
 )

# Qt4

FIND_PACKAGE( Qt4 )
SET( QT_USE_QTGUI TRUE )
SET( QT_USE_QTOPENGL TRUE )
INCLUDE( ${QT_USE_FILE} )

MACRO( WRAP_PYTHON_UI )
  FOREACH( input_file ${ARGN} )
    ADD_CUSTOM_COMMAND (
      OUTPUT tools/ui/ui_${input_file}.py
      COMMAND pyside-uic tools/ui/${input_file}.ui -o tools/ui/ui_${input_file}.py
      DEPENDS tools/ui/${input_file}.ui
      COMMENT "Generating tools/ui/ui_${input_file}.py from tools/ui/${input_file}.ui"
    )
    ADD_CUSTOM_TARGET(ui_${input_file} ALL DEPENDS tools/ui/ui_${input_file}.py )
  ENDFOREACH( input_file )
ENDMACRO( WRAP_PYTHON_UI )
WRAP_PYTHON_UI( guiAGGLEditor guiGraphViewer appearance )

[[[cog
A()
if component['gui'] != 'none':
	cog.out('WRAP_PYTHON_UI( src/mainUI.ui )')
Z()
]]]
[[[end]]]
