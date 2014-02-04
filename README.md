BoS
===

build_on_save (BoS) is a simple python script that utilises a python implementation of Linux's kernal service 'inotify', called 'pyinotify'. It watches a directory for changes to files and runs bash commands on them if they are modified.

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

6. Start the BOS watcher via the shell command:
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
