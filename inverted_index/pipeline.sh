#!/bin/bash
#
# Example of how to chain MapReduce jobs together.  The output of one
# job is the input to the next.
#
# Hadoop (or Madoop) options
# jar index/hadoop/hadoop-streaming-2.7.2.jar   # Hadoop configuration
# -input <directory>                            # Input directory
# -output <directory>                           # Output directory
# -mapper <exec_name>                           # Mapper executable
# -reducer <exec_name>                          # Reducer executable

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

# Optional input directory argument
PIPELINE_INPUT=input
if [ -n "${1-}" ]; then
  PIPELINE_INPUT="$1"
fi

# Print commands
set -x

# Remove output directories
rm -rf output output[0-9]

# Job 0: Document Count (this job is not part of the pipeline)
madoop \
  -input ${PIPELINE_INPUT} \
  -output output0 \
  -mapper ./map0.py \
  -reducer ./reduce0.py

# Copy document count to a separate file
cp output0/part-00000 total_document_count.txt

# Job 1
madoop \
  -input ${PIPELINE_INPUT} \
  -output output1 \
  -mapper ./map1.py \
  -reducer ./reduce1.py

# Job 2
madoop \
  -input output1 \
  -output output2 \
  -mapper ./map2.py \
  -reducer ./reduce2.py

# Job 3
madoop \
  -input output2 \
  -output output3 \
  -mapper ./map3.py \
  -reducer ./reduce3.py

# Job 4
madoop \
  -input output3 \
  -output output4 \
  -mapper ./map4.py \
  -reducer ./reduce4.py

# Job 5
madoop \
  -input output4 \
  -output output5 \
  -mapper ./map5.py \
  -reducer ./reduce5.py

# Job 6
madoop \
  -input output5 \
  -output output \
  -mapper ./map6.py \
  -reducer ./reduce6.py

cp output/part-00000 ../index_server/index/inverted_index/inverted_index_0.txt
cp output/part-00001 ../index_server/index/inverted_index/inverted_index_1.txt
cp output/part-00002 ../index_server/index/inverted_index/inverted_index_2.txt