#!/bin/bash

version="v0.0.1"
timestamp=$(date +"%Y-%m-%d-%H%M%S")
zip_name="klms-addon-$version-$timestamp.zip"

cd src
mkdir "../dest/klms-addon-$version-$timestamp"
cp -r * "../dest/klms-addon-$version-$timestamp/"
cd ../dest
zip -r "$zip_name" "klms-addon-$version-$timestamp"
rm -r "klms-addon-$version-$timestamp"

