#!/bin/bash

JSON_FILE=$1
OUT_DIR=$2

if [ -d $OUT_DIR ]
then
  rm $OUT_DIR/*
else
  mkdir $OUT_DIR
fi

if [ -d $OUT_DIR/rgba ]
then
  rm $OUT_DIR/rgba/*
else
  mkdir $OUT_DIR/rgba
fi

if [ -d $OUT_DIR/bump ]
then
  rm $OUT_DIR/bump/*
else
  mkdir $OUT_DIR/bump
fi

/Applications/Rebelle\ 7\ Motion\ IO.app/Contents/MacOS/Rebelle\ 7\ Motion\ IO -no-gui -batch-json $JSON_FILE -batch-out-rgba $OUT_DIR/rgba/bgs_rgba.####.exr -batch-out-bump $OUT_DIR/bump/bgs_bump.####.exr -batch-start-frame-number 200

#/Applications/Rebelle\ 7\ Motion\ IO.app/Contents/MacOS/Rebelle\ 7\ Motion\ IO -no-gui -batch-json $JSON_FILE -batch-out-rgba_canvas $OUT_DIR/####.png -batch-start-frame-number 200

# Convert *.exr files to mp4
#image_size="1920x1080"
#num_frames=$(ls "$OUT_DIR"/*.png | wc -l)
#framerate=25
#duration=$(echo "scale=2; $num_frames / $framerate" | bc)
#ffmpeg -y -framerate $framerate -i "$OUT_DIR/%04d.png" -vf "color=white:size=${image_size} [bg]; [bg][0:v] overlay" -c:v libx264 -preset slow -crf 18 -t "$duration" "$OUT_DIR.mp4"
