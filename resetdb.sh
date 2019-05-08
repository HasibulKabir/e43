#!/bin/bash
echo "Resetting database..."
for i in counters/*.txt
do
  echo "0" > $i
done
echo "0" > random.txt
rm -f extras/*.txt
rm -f deadlines/*.txt
>tags.txt
>chatids.txt
>chatids2.txt
>counters-disabled.txt
>subsoff.txt
echo "Done!"
