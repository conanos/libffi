#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from cpt.packager import ConanMultiPackager

__PACKAGE_NAME__ = 'libffi'
PATTERN_ = re.compile(r'conanio/(?P<compiler>gcc|clang)(?P<version>\d+)(-(?P<arch>\w+))?')

if __name__ == "__main__":

    docker_entry_script = ''
    m = PATTERN_.match(os.environ.get('CONAN_DOCKER_IMAGE',''))
    if m:
        docker_entry_script = '/bin/bash docker_entry_script.sh {compiler} {version}'.format(
            compiler = m.group('compiler'), version = m.group('version') )
        
    builder = ConanMultiPackager(docker_entry_script=docker_entry_script)
    builder.add_common_builds(pure_c=True)

#    filter(__PACKAGE_NAME__,builder)
    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        if options["libffi:shared"] == True and settings["arch"] == "x86_64":
             filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    
    builder.run()


#from bincrafters import build_template_default
#import platform
#import os
#from conanos.sdk.profile import filter
#if platform.system() == 'Windows':
#    os.environ['CONAN_VISUAL_VERSIONS']=os.environ.get('CONAN_VISUAL_VERSIONS','15')
#
#PACKAGE_NAME='libffi'	
#if __name__ == "__main__":
#    builder = build_template_default.get_builder()
#    filter(PACKAGE_NAME,builder)
#
#    builder.run()
