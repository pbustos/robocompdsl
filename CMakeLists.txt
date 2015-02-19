cmake_minimum_required( VERSION 2.8)


#  Installation  #
##################

INSTALL(PROGRAMS "parseCDSL.py" DESTINATION /opt/robocomp/python)
INSTALL(PROGRAMS "parseIDSL.py" DESTINATION /opt/robocomp/python)
INSTALL(PROGRAMS "robocompdsl.py" DESTINATION /opt/robocomp/bin RENAME robocompdsl )

