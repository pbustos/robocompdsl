cmake_minimum_required( VERSION 2.8 )

SUBDIRS( src )

INSTALL(FILES etc/config DESTINATION /opt/robocomp/etc-default/ RENAME
[[[cog
A()
cog.out(' ' + component['name'])
Z()
]]]
[[[end]]]
.conf )

ADD_CUSTOM_TARGET(doc doxygen Doxyfile)
ADD_CUSTOM_TARGET(installdoc mkdir -p /opt/robocomp/doc COMMAND cp -R doc/html /opt/robocomp/doc/

[[[cog
A()
cog.out( component['name'] + ' ')
Z()
]]]
[[[end]]]
)