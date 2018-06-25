#!/bin/bash
echo "Resetting database..."
for i in counters/*.txt
do
  echo "0" > $i
done
echo "0" > random.txt
rm -f extras/*.txt
>tags.txt
>chatids.txt
>counters-disabled.txt
echo "Done!"
