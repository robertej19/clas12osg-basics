#!/bin/bash

dir="database/"
file="database/CLAS12OSG.db"

if [ -d "$dir" ] ; then
	echo "Database Directory Exists"
	if [ -f  "$file" ] ; then
		echo "SQLite DB File Exists, Removing" 
		rm $file
	fi
else
	echo "Creating database directory"
	mkdir -p $dir
fi

mkdir database/
cd common_tools/
python3 create_database.py --lite=../database/CLAS12OSG.db
cd ../client/
python3 src/SubMit.py --lite=../database/CLAS12OSG.db -u=testuser scards/scard_type1.txt
sqlite3 ../database/CLAS12OSG.db 'SELECT user,run_status,client_time FROM submissions;'
