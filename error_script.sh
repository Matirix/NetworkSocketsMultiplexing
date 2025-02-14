#!/bin/bash

commands=(
    "Empty arguments|python3 ./client.py"
    "Invalid Port number (Letter) | python3 ./client.py -i 127.0.0.1 -p l33 -k aaa -f test1.txt"
    "Invalid Port number (Outside of range) | python3 ./client.py -i 127.0.0.1 -p 100000 -k aaa -f test1.txt"
    "Invalid Address (Missing dot)|python3 ./client.py -i 127.011 -p 3333 -k aaa -f test1.txt"
    "Invalid Address (Not a digit)|python3 ./client.py -i 127.0.0.z -p 3333 -k aaa -f test1.txt"
    "Invalid Key (Has numbers)|python3 ./client.py -i 127.0.0.1 -p 3333 -k a2a -f test1.txt"
    "Invalid File (File not found)|python3 ./client.py -i 127.0.0.1 -p 3333 -k aaa -f 404.txt"
    "Client is only run with valid arguments|python3 ./client.py -i 127.0.0.1 -p 3333 -k aaa -f test1.txt"
)

index=1
clear
for cmd in "${commands[@]}"; do
    title="${cmd%%|*}"
    command="${cmd#*|}"

    echo -e "\nTest #$index :$title"
    echo "Running: $command"
    eval "$command"
    sleep 3
    clear
    ((index++))
done
