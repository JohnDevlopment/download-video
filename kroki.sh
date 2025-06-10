#!/bin/bash

declare -r BASENAME=$(basename $(realpath "$0"))

## usage: die MSG [CODE]
function die {
    echo -e "$BASENAME: $1" >&2
    exit ${2:-1}
}

## usage: quote ARG
function quote {
    local arg
    arg="$1"
    if [ -z "$arg" ]; then
	echo "missing ARG" >&2
	return 1
    fi
    printf "%q" "$arg"
}

cd design-doc_files || exit 1

file=$(dir -1 | fzf)

case "$file" in
    *.pum)
	outfile=${file%.pum}.png
	format=plantuml
	;;
    *)
	die "Invalid file"
esac

kroki convert -t $format -o "$outfile" "$file"
echo -n kroki convert -t $format -o $(quote "design-doc_files/$outfile") \
     $(quote "design-doc_files/$file") | xclip -selection clipboard
