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

# Add to /etc/hosts
while IFS= read -r domain_name; do
    echo "127.0.0.1 $domain_name" | sudo tee -a /etc/hosts > /dev/null
    #echo "Host added: 127.0.0.1 $domain_name"
done < "$full_path"
