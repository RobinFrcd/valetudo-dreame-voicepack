#!/bin/bash

# Parse the command line arguments
convert_flag=false
while getopts "ci:o:" opt; do
    case ${opt} in
        c )
            convert_flag=true
            ;;
        i )
            input_dir=${OPTARG}
            ;;
        o )
            pack_name=${OPTARG}
            ;;
  \? )
    echo "Invalid Option: -$OPTARG" 1>&2
    exit 1
    ;;
 esac
done

# The output directory where the ogg files will be saved
output_dir="${input_dir}/../ogg"
norm_dir="${input_dir}/../wav-norm"

# Create the output directory if it doesn't exist

rm -rf $output_dir
rm -rf $norm_dir
mkdir -p "$output_dir"
mkdir -p "$norm_dir"
echo $convert_flag
echo $input_dir
echo $pack_name

# Loop through all the wav files in the input directory
for file in "$input_dir"/*.{wav,mp3}; do
    # Get the base name of the file without the extension
    base_name="$(basename "$file")"
    base_name="${base_name%.*}"
    if [[ $convert_flag == true ]]; then
        ffmpeg -i "${file}" -filter:a "loudnorm=I=-5:LRA=1:dual_mono=true:tp=-1, volume=4" "$norm_dir/$base_name.wav"
        oggenc "$norm_dir/$base_name.wav" --output "$output_dir/$base_name.ogg" --bitrate 100 --resample 16000
    else
        ffmpeg -i ${file} -acodec libvorbis -b:a 100k -ar 16000 -af "volume=8dB" "$output_dir/$base_name.ogg"
    fi
done

root_dir=$(pwd)
cd $output_dir
tar -czf ${root_dir}/${pack_name}.tar.gz *.ogg
cd ${root_dir}

md5sum ${pack_name}.tar.gz
