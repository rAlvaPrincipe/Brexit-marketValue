#!/bin/bash

wget  https://www.dropbox.com/s/x93vq030dhtvuro/Brexit.zip
unzip Brexit.zip && rm Brexit.zip
rm  -rf __MACOSX 
mv brexit.sql ../datasets/
mv GBP_EUR.txt ../datasets/