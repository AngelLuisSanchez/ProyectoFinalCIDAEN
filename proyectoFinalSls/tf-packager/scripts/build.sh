#!/bin/bash

build () {

. /venv/bin/activate

pip install --upgrade --ignore-installed --no-cache-dir requests==2.19.1
pip install --upgrade --ignore-installed --no-cache-dir beautifulsoup4==4.6.1
pip install --upgrade --ignore-installed --no-cache-dir lxml==4.2.4
deactivate

# Add __init__.py to google dir to make it a package
touch /venv/lib64/python3.6/site-packages/google/__init__.py

# Remove *.so binaries to save space
find /venv/lib/python3.6/site-packages -name "*.so" | xargs strip
find /venv/lib64/python3.6/site-packages -name "*.so" | xargs strip

# Zip libraries
mkdir -p $(dirname "${output}")

dirs=("/venv/lib/python3.6/site-packages/" "/venv/lib64/python3.6/site-packages/")

for dir in "${dirs[@]}"
  do
  	cd ${dir}
  	rm -rf easy_install* pip* setup_tools* setuptools* wheel*    # Remove unnecessary libraries to save space
  	zip -r9q /tmp/lambda_package.zip * --exclude \*.pyc
  done
}

build