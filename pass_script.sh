#!/bin/bash

commands=(
    "Viegenere Cipher (Includes both lower and upper) |test1.txt |  python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test1.txt"
    "Viegenere Cipher (Content Wraps Around) |test2.txt | python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test2.txt"
    "Viegenere Cipher (Ignores special characters + numbers) |test3.txt | python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test3.txt"
    "Viegenere Cipher (Accepts different extension [.html])|test4.html | python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test4.html"
    "Viegenere Cipher (Payload contains more than one delimiter) |test5.txt | python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test5.txt"
    "Server handles more than one client (2 clients) |test1.txt test1.txt | python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test1.txt & python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test1.txt "
    "Server handles more than one client (5 clients) |test1.txt test2.txt test3.txt test4.html test5.txt |python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test1.txt & python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test2.txt & python3 ./client.py -i 127.0.0.1 -p 3333 -k aba -f test3.txt & python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test4.html & python3 ./client.py -i 127.0.0.1 -p 3333 -k bbbb -f test5.txt"
)

index=1
clear
for cmd in "${commands[@]}"; do
    # Get everything before the first pipe
    title="${cmd%%|*}"

    # Get everything after the first pipe, and then before the second pipe
    filecontent="${cmd#*|}"
    filecontent="${filecontent%%|*}"

    # Get everything after the last pipe
    command="${cmd#*|*|}"
    command="${command%%|*}"

    echo -e "TEST #$index :$title"
    echo "FILE CONTENT:"
    eval "cat $filecontent"
    echo "COMMAND: $command"
    eval "$command"
    wait
    sleep 5
    clear
    ((index++))
done
