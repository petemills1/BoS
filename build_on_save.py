#!/usr/bin/env python

"""
build_on_save (BoS) is a simple python script that utilises a python
implementation of Linux's kernal service 'inotify', called
'pyinotify'. It watches a directory for changes to files
and runs bash commands on them if they are modified.

1. If the modified file is a .sass file then BoS runs
'rapydcss' on the modified file, to compile a .css file from 
it. 

2. If the modified file is a .pyj file then BoS runs 
'rapydscript' on the modified file, to compile a .js file 
from it.

To use BoS:

    1. Install pyinotify via the shell command:
        'pip install --upgrade pyinotify'
    Note: Install pyinotify OUTSIDE of your virtual environment

    2. Save BoS to a safe directory.

    3. Navigate to the directory BoS is located in.

    4. Run the shell command:
        'chmod +x build_on_save.py'

    5. Open a new terminal window

    6. Start the BoS watcher via the shell command:
        'build_on_save.py /path/to/your/directory'

    7. Exit the watcher using Ctrl + C

NOTES:
To avoid annoying warnings that may appear when using rapydcss,
the libpcre3-dev library must be installed. If you already have
rapydcss installed and are getting warnings of the kind: 
' Scanning acceleration disabled (_speedups not found)!', then 
run the following two shell commands:
    'sudo apt-get install libpcre3-dev'
    'sudo pip install rapydcss --force-reinstall -I'
"""

import os, sys, pyinotify, subprocess
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_CLOSE_WRITE

def Monitor(path):

    class PClose_Write(ProcessEvent):
            
        def process_IN_CLOSE_WRITE(self, event):
            
            modified_path = str(event.pathname)
            file_name = []
            for i in reversed(modified_path):
                if i == '/':
                    break
                file_name.append(i)

            file_name = ''.join(file_name)

            reversed_string = ''
            for i in range(len(file_name)-1,-1,-1):
                reversed_string += file_name[i]

            file_name = reversed_string

            if "sass" in file_name:
                print '\nSASS--File:', file_name, 'modified', '- Calling rapydcss on: ' + event.path + '/' + file_name + '\n'
                subprocess.call('rapydcss ' + event.path + '/' + file_name, shell=True)
                
            elif "pyj" in file_name:
                file_name_js = ''
                for i in file_name:
                    if i == '.':
                        break
                    file_name_js += i
                file_name_js  = file_name_js + '.js'

                print '\nPYJ--File:', file_name, 'modified', '- Calling rapydscript on: ' + event.path + '/' + file_name + '\n'

                subprocess.call('rapydscript ' + event.path + '/' + file_name \
                  + ' -o ' + event.path + '/' + file_name_js, shell=True)
            else:
                print 'IGNORED--File:', file_name, 'modified. This file type is not accounted for. No action taken \n'

    sub_dirs = []
    if monitor_all == '-r':
        sub_dirs = [sub_dir for sub_dir in os.listdir(path) 
          if os.path.isdir(os.path.join(path, sub_dir))]
    elif monitor_all != None:
        print '\nInvalid command. You typed: `' + monitor_all + '` Did you mean `-r`? Use `-r` to force BoS to watch for changes in all sub directories of ' + path
        sys.exit()

    wm = WatchManager()
    notifier = Notifier(wm, PClose_Write())
    wm.add_watch(path, pyinotify.IN_CLOSE_WRITE)
    if monitor_all == '-r':
        for sub_dir in sub_dirs:
            wm.add_watch(path + '/' + sub_dir, pyinotify.IN_CLOSE_WRITE)

    print '\n---------------------------'
    print 'BoS is locked and loaded!'
    print 'Waiting for movement in:', path
    if monitor_all == '-r':
        print '\nWith sub directories: '
        for sub_dir in sub_dirs:
            print '\n',sub_dir
    print '---------------------------'

    try:
        while 1:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
    except KeyboardInterrupt:
        print '\n---------------------------'
        print 'Exiting BoS...'
        print '---------------------------'
        notifier.stop()
        return

if __name__ == '__main__':
    try:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            monitor_all = sys.argv[2]
        else:
            monitor_all = None
    except IndexError:
        print 'Invalid directory index'
    else:
        Monitor(path)
