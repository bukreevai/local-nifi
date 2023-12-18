#!/bin/bash

# Hostnames file
script_dir="$(dirname "$0")"
file="hosts_list.txt"
full_path="$script_dir/$file"

# File exists?
if [ ! -f "$full_path" ]; then
    echo "File $file not found!"
    exit 1
fi

while IFS= read -r domain; do
    # Remove host from /etc/hosts
    sudo sed -i '' "/$domain/d" /etc/hosts
    echo "Hosts delete: $domain"
done < "$full_path"