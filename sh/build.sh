#!/bin/bash

version="v0.0.1"
home_dir="/home/$USER"
kodi_dir="$home_dir/_Tmp"
project_dir="$home_dir/Development/Kodi/kodi_lms_now_playing"
src_dir="$project_dir/addon"
timestamp=$(date +"%Y-%m-%d-%H.%M.%S")

build_sub_dir=""

case "$1" in
  "working")
    build_sub_dir="working"
    ;;
  *)
    build_sub_dir="test"
    ;;
esac

build_dir="$project_dir/build/$build_sub_dir"
addon_name="klms-addon-$version-$timestamp"
temp_build_dir="$build_dir/$addon_name"
zip_name="$addon_name.zip"

echo "Building zip file for Kodi..."
mkdir $temp_build_dir
cp -r $src_dir/* $temp_build_dir
cd $build_dir
zip -r $zip_name $addon_name
rm -r $addon_name
rm -rf "$kodi_dir"/*.zip
cp $zip_name $kodi_dir
cd $project_dir
echo "Build complete!"

