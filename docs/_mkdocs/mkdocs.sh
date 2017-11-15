#!/bin/sh

cd ../../
virtualenv env
. env/bin/activate
pip install -r requirements.txt

cd -
sphinx-apidoc -o pyArborSP ../../

make clean
make dirhtml

rsync -avz _build/dirhtml/ ../

cd ../../
deactivate
rm -rf env
