#!/usr/bin/env bash

keeptmp=
queue="default"
gpuflag="gpu='NO'"

while getopts akq:g optname
do
    case $optname in
	k)
	    keeptmp=1
	    ;;
	q)
	    queue="$OPTARG"
	    ;;
	g)
	    gpuflag="gpu='NO'"
	    ;;
	a)
	    gpuflag="gpu LIKE '%'"
	    ;;
	*)
	    printf "Unknown option $optname\n"
	    printf "Usage: %s: [-k] [-q <queue>] -g\n" $0
	    printf "\t -k: keep temporary files\n"
	    printf "\t -q<queue> submit in queue <queue>\n"
	    printf "\t -g: submit on gpu nodes\n"
	    exit 2;
	    ;;
    esac
done

nb_test=$(ctest -N | tail -1 | awk '{print $3;}')

testname="testtomo3d"

rm -vf OAR.$testname.*.stdout
rm -vf OAR.$testname.*.stderr

bindir=`dirname $0`

sdate=`date`
oarsub --array $nb_test -n $testname --scanscript $bindir/submit_test_licallo.oar --queue $queue -p "$gpuflag" > ./licallotljobs.log

#depline=$(for j in $(echo "$qmsg" | grep "OAR_JOB_ID=" | sed -e 's/.*OAR_JOB_ID\=//g')
#do
#  echo -n "-a $j "
#done)
#oarsub -n analyzis -l walltime="0:1:0" $depline --notify "mail:alain.miniussi@oca.eu" --scanscript $bindir/analyze_test_licallo.oar

logfile=./licallotests.log
resfile=./licallotres.log

oarstat > $logfile
while [[ -s $logfile  ]] ; do
  sleep 1
#//  echo "    ****************  "
  cat OAR.$testname.*.stdout 2> /dev/null | egrep "^1/1 Test" > $resfile 
  failed=$(grep -i -v Passed $resfile | wc -l )
  passed=$(grep -i Passed $resfile | wc -l )
  echo -n -e "\r>>>>> $passed passed, $failed failed, $(expr $nb_test \- $passed \- $failed) waiting"

  oarstat | grep $testname > $logfile
  for s in $(cat $logfile | awk '{ print $6; }' | sort -u); do
      echo -n " $s: $(cat $logfile | awk '{ print $6; }' | grep $s | wc -l), "
  done
  echo -n "         "
done

edate=`date`
echo "started at $sdate, finished at $edate"

cat OAR.$testname.*.stdout | egrep "^1/1 Test" > $resfile

failed=$(grep -v -i Passed $resfile | wc -l )
passed=$(grep -i Passed $resfile | wc -l )

echo "Passed $passed and failed $failed out of $nb_test"
nb_weird=$(expr $nb_test \- $passed \- $failed)
if [[ $nb_weird -ne 0 ]]; then
    echo "but $nb_weird got lost ???"
fi
grep -i Failed $resfile

if [ -z $keeptmp ]
then
    rm -f OAR.$testname.*.stdout
    rm -f OAR.$testname.*.stderr
fi