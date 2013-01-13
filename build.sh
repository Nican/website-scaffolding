#!/bin/bash
mkdir content/guides/kalman1
cp pregen/kalman1/static/* content/guides/kalman1/
cd pregen/kalman1
python ../htmlatex.py kalman1.markup ../../content/guides/kalman1/index.html ../../content/guides/kalman1/ kalman1/
cd ../..
mv content/guides/kalman1/kalman1.py content/guides/kalman1/kalman1.py.txt
mv content/guides/kalman1/kalman2.py content/guides/kalman1/kalman2.py.txt
hyde gen