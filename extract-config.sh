#!/bin/bash

DOWNLOADS="$HOME/Downloads"
DESTINATION="$DOWNLOADS/artbeads_storefront_theme"
project_folder=${1:-"$HOME/work/artbeads-bigcommerce"}

if ! [ -d "$project_folder" ]; then
    echo "'$project_folder' does not exist"
    exit 1
fi

chiara_zip_filename=$(ls "$DOWNLOADS" | grep "Chiara")

if [ -z $chiara_zip_filename ]; then
    echo "Chiara does not exists in 'Downloads'"
    exit 1
fi

rm -rf "$DESTINATION"
mkdir -p "$DESTINATION"

mv "$DOWNLOADS/$chiara_zip_filename" "$DESTINATION/$chiara_zip_filename"

cd "$DESTINATION"
unzip "$DESTINATION/$chiara_zip_filename"

cp ./config.json "$project_folder"

rm -rf "$DOWNLOADS/$chiara_zip_filename"
