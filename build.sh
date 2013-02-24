#!/bin/bash
if [ `uname` == 'Darwin' ]
  then
    alias python='python2.7-32'
fi
# Kalman1 stuff
mkdir content/guides/kalman1
cp pregen/kalman1/static/* content/guides/kalman1/
cd pregen/kalman1
python ../htmlatex.py kalman1.markup ../../content/guides/kalman1/index.html ../../content/guides/kalman1/ ./
cd ../..
mv content/guides/kalman1/kalman1.py content/guides/kalman1/kalman1.py.txt
mv content/guides/kalman1/kalman2.py content/guides/kalman1/kalman2.py.txt

# Kalman 2 stuff
mkdir content/guides/kalman2
cp pregen/kalman2/static/* content/guides/kalman1/
cd pregen/kalman2
python ../htmlatex.py kalman2.markup ../../content/guides/kalman2/index.html ../../content/guides/kalman2/ ./
cd ../..

hyde gen