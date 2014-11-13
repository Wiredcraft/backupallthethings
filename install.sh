#!/bin/bash
##################
# devo.ps backup collection
##################
# Description:
#  Collection of scripts to perform various backup operation for the services
#  supported by devo.ps
##################

DEST=/opt/devops/backup

# Copy the config and various scripts to the destination 
mkdir -p $DEST
for folder in conf scripts-available bin
do
    cp -a $folder $DEST
done

# Make the various scripts executable
chmod +x $DEST/bin/*
chmod +x $DEST/scripts-available/*

# Link master backup script
ln -s $DEST/bin/backup /usr/local/bin