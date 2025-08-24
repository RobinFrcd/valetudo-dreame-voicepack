#!/bin/bash

# Initialize norm_flag to false by default
norm_flag=false

# Parse the command line arguments
# The colon after "n" is removed, making it a simple flag.
while getopts "i:o:n" opt; do
    case ${opt} in
        i )
            input_dir=${OPTARG}
            ;;
        o )
            pack_name=${OPTARG}
            ;;
        n )
            # When -n is present, set the flag to true. It doesn't use OPTARG.
            norm_flag=true
            ;;
        \? )
            echo "Invalid Option: -$OPTARG" 1>&2
            exit 1
            ;;
    esac
done

# Check if required arguments were provided
if [ -z "$input_dir" ] || [ -z "$pack_name" ]; then
    echo "Usage: $0 -i <input_directory> -o <pack_name> [-n]"
    exit 1
fi

# The output directory where the ogg files will be saved
output_dir="${input_dir}/../ogg"

rm -rf "$output_dir"
mkdir -p "$output_dir"
echo "Input directory: $input_dir"
echo "Output pack name: $pack_name"
echo "Normalization enabled: $norm_flag"

# Loop through all the mp3 files in the input directory
for file in "$input_dir"/*.{mp3,wav}; do
    # Get the base name of the file without the extension
    base_name="$(basename "$file")"
    base_name_no_ext="${base_name%.*}"

    # This if-statement now works correctly with the true/false flag
    if [ "$norm_flag" = true ]; then
        echo "Normalizing and converting $base_name..."
        ffmpeg -hide_banner -loglevel error -i "${file}" \
            -acodec libvorbis \
            -q:a 8 \
            -ar 16000 \
            -af "loudnorm=I=-16:TP=-0.1:LRA=11" \
            "$output_dir/$base_name_no_ext.ogg"
    else
        echo "Converting $base_name..."
        ffmpeg -hide_banner -loglevel error -i "${file}" \
            -acodec libvorbis \
            -q:a 8 \
            -ar 16000 \
            "$output_dir/$base_name_no_ext.ogg"
    fi
done

echo "Creating tarball..."
root_dir=$(pwd)
cd "$output_dir" || exit
tar -czf "${root_dir}/${pack_name}.tar.gz" *.ogg
cd "${root_dir}" || exit

echo "Done. MD5 checksum:"
md5sum "${pack_name}.tar.gz"
