#!/bin/bash
echo "Resetting database..."
for i in counters/*.txt
do
  echo "0" > $i
done
git checkout -- extras/
git checkout -- tags.txt
git checkout -- chatids.txt
echo "Done!"
