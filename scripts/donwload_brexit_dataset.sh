#!/bin/bash

wget  https://www.dropbox.com/s/x93vq030dhtvuro/Brexit.zip
unzip Brexit.zip 
rm  -rf __MACOSX 
rm Brexit.zip
mv brexit.sql ../datasets/
mv GBP_EUR.txt ../datasets/