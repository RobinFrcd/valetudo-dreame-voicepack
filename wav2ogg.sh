#!/bin/bash

# The input directory containing the wav files
input_dir="$1"
pack_name="$2"

# The output directory where the ogg files will be saved
output_dir="${input_dir}/../ogg"
norm_dir="${input_dir}/../wav-norm"

# Create the output directory if it doesn't exist
rm -rf $output_dir
rm -rf $norm_dir
mkdir -p "$output_dir"
mkdir -p "$norm_dir"

# Loop through all the wav files in the input directory
for file in "$input_dir"/*.wav; do
    # Get the base name of the file without the extension
    base_name=$(basename "$file" .wav)

    ffmpeg -i "${file}" -filter:a "loudnorm=I=-5:LRA=1:dual_mono=true:tp=-1, volume=4" "$norm_dir/$base_name.wav"
    oggenc "$norm_dir/$base_name.wav" --output "$output_dir/$base_name.ogg" --bitrate 100 --resample 16000
done

root_dir=$(pwd)
cd $output_dir
tar -czf ${root_dir}/${pack_name}.tar.gz *.ogg
cd ${root_dir}

md5sum ${pack_name}.tar.gz
