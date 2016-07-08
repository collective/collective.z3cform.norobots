#!/bin/bash
# ./test-set-buildout.sh 5.0.x
# ./test-set-buildout.sh 4.3.x
# ===> change and execute buildout
# ./test-set-buildout.sh 5.0.x clean
# ./test-set-buildout.sh 4.3.x clean
# ===> ATTENTION: remove the Data.fs file, remove virtualenv files, change and execute buildout

function print()
{
    echo ''
    echo '================================================'
    echo $1
    echo '================================================'
    echo ''
}

if [ $2 == clean ]; then
    if [ -f var/filestorage/Data.fs ]; then
        print "Remove Data.fs file"
        rm var/filestorage/Data.fs
  fi
  if [ -f bin/python ]; then
      print "Remove virtualenv files"
      rm -rf bin develop-eggs include lib parts var
  fi
fi

if [ ! -f bin/python ]; then
    print "Install a virtual in the current directory"
    virtualenv .
    source bin/activate
    easy_install -U zc.buildout
    easy_install -U distribute
fi

print "Change buildout for test-plone-$1.cfg"
if [ -f buildout.cfg ]; then
    rm buildout.cfg
fi
ln -s test-plone-$1.cfg buildout.cfg

print "Lauch buildout"
python bootstrap.py
bin/buildout

print "Lauch Zope instance"
./bin/instance fg
