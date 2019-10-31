#!/bin/bash
echo "Syncing data from /vagrant"
cp -r /vagrant/ecoh .
cp -r /vagrant/Singularity .
cp /vagrant/deploy_scripts/* $HOME/bin
chmod -R 755 $HOME/bin
echo "Syncing complete"
