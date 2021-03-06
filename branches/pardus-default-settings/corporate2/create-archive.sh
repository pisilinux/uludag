#!/bin/bash

NAME=pardus-default-settings
VERSION=0.1.6

DIRNAME=$NAME-$VERSION

if [ -d ../$DIRNAME ]; then
    echo ../$DIRNAME already exists. Remove it first.
    exit 1
fi

cp -r . ../$DIRNAME
tar czvf $DIRNAME-corporate2.tar.gz ../$DIRNAME --exclude .svn --exclude `basename $0`
rm -rf ../$DIRNAME
