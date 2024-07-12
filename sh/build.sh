#!/bin/bash

home_dir="/home/n4lbm"
root_dir="$home_dir/Development/Kodi/kodi_lms_now_playing"
src_dir="$root_dir/src"
dest_dir="$root_dir/dest"
version="v0.0.1"
timestamp=$(date +"%Y-%m-%d-%H.%M.%S")
addon_name="klms-addon-$version-$timestamp"
temp_build_dir="$dest_dir/$addon_name"
zip_name="$addon_name.zip"
kodi_dir="$home_dir/_Tmp"

echo "Building zip file for Kodi..."
mkdir $temp_build_dir
cp -r $src_dir/* $temp_build_dir
cd $dest_dir
zip -r $zip_name $addon_name
rm -r $addon_name
cp $zip_name $kodi_dir
cd $root_dir
echo "Build complete!"

