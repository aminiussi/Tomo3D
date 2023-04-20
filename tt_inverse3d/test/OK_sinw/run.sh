#!/usr/bin/env bash

nb_cpu=$(grep -i "physical id" /proc/cpuinfo | sort -u | wc -l)
nb_core=$(grep -i "sibling" /proc/cpuinfo | sort -u | awk '{print $3;}')

srcdir=$1
bindir=$2
mpi_prefix=$3

set -x 

if [[ ! -d $bindir ]]; then mkdir $bindir; fi

cp $srcdir/basic.job $bindir/
jobscript=$srcdir/run.job

if [[ ! -x $jobscript ]]; then
    echo "$jobscript does not exist or is not executale"
fi

cd $bindir
rm -rf $bindir/output
mkdir $bindir/output

$jobscript -s $srcdir/input -p "$mpi_prefix" -t $nb_core -b $bindir

job_status=$?
if [ $job_status -ne 0 ]; then
    echo "job failed with status $job_status"
    exit $job_status
fi

check_output=$srcdir/../check_output.py
output_status=0

verbose=""

if [ -n "$verbose" ]
then
    smesh_tot=$(ls $srcdir/gold/*smesh* | wc -l)
    smesh_failed=0
    for o in $(ls $srcdir/gold/*smesh*); do
	fname=$(basename $o)
	$check_output $srcdir/gold/$fname $bindir/output/$fname --format=smesh --nb-errors=50 --diff=$bindir/output/$fname.diff
	ostatus=$?
	if [ $ostatus -ne 0 ]; then
	    let smesh_failed++
	    echo "got mistmatch on output $fname"
	else
	    echo "$fname matches"
	fi
    done
    
    refl_tot=$(ls $srcdir/gold/*refl* | wc -l)
    refl_failed=0
    for o in $(ls $srcdir/gold/*refl*); do
	fname=$(basename $o)
	$check_output $srcdir/gold/$fname $bindir/output/$fname --format=refl --nb-error=50 --diff=$bindir/output/$fname.diff
	ostatus=$?
	if [ $ostatus -ne 0 ]; then
	    let refl_failed++
	    echo "got mistmatch on output $fname"
	else
	    echo "$fname matches"
	fi
    done
    
    ray_tot=$(ls $srcdir/gold/*ray* | wc -l)
    ray_failed=0
    for o in $(ls $srcdir/gold/*ray*); do
	fname=$(basename $o)
	$check_output $srcdir/gold/$fname $bindir/output/$fname --format=ray --nb-error=50 --diff=$bindir/output/$fname.diff
	ostatus=$?
	if [ $ostatus -ne 0 ]; then
	    let ray_failed++
	    echo "got mistmatch on output $fname"
	else
	    echo "$fname matches"
	fi
    done
    
    tres_tot=$(ls $srcdir/gold/*tres* | wc -l)
    tres_failed=0
    for o in $(ls $srcdir/gold/*tres*); do
	fname=$(basename $o)
	$check_output $srcdir/gold/$fname $bindir/output/$fname --format=tres --nb-error=50 --diff=$bindir/output/$fname.diff
	ostatus=$?
	if [ $ostatus -ne 0 ]; then
	    let tres_failed++
	    echo "got mistmatch on output $fname"
	else
	    echo "$fname matches"
	fi
    done
fi

log_failed=0
for o in $(ls $srcdir/gold/*.log); do
    fname=$(basename $o)
    $check_output --format log $srcdir/gold/$fname $bindir/output/$fname --format=log --diff=$bindir/output/$fname.diff --nb-relaxed=2
    ostatus=$?
    if [ $ostatus -ne 0 ]; then
	let log_failed++
	echo "got mistmatch on output $fname"
    else
	echo "$fname matches"
    fi
done

if [ -n "$verbose" ]
then
    echo "SMESH $smesh_failed failed out of $smesh_tot"
    echo "REFL $refl_failed failed out of $refl_tot"
    echo "RAY $ray_failed failed out of $ray_tot (ignored)"
    echo "TRES $tres_failed failed out of $tres_tot"
fi
echo "LOG $log_failed failed"

failed=0
let failed=$smesh_failed+$refl_failed+$tres_failed+$log_failed

if [ $failed -ne 0 ]; then
    echo "Total failed: $failed"
    exit 1
else
    exit 0
fi
