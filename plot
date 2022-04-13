#
# format of data.txt:
# solver variables forget clauses size memory time secs
#
# timeouts are converted to values over the maximum obtained for real time and
# size; they are omitted in all other cases

VARS=8
VARS=10
SOLVERS=linear
# SOLVERS='close eliminate linear backtrack'
DATADIR=${HOME}/temp/square

FSOLVER=1
FVARIABLES=2
FFORGET=3
FCLAUSES=4
FSIZE=5
FMEMORY=6
FTIME=7
FSECS=8
FKB=9

# cd

cd "$DATADIR"


# plot all solvers

for SOLVER in $SOLVERS;
do


# variables -> secs (real time)

echo "$SOLVER variables->secs"

grep "^$SOLVER " random-* | \
sed 's,TIMEOUT *TIMEOUT$,10.0 14000,g' > data.txt

gnuplot <<-!

	set terminal png
	#set xrange [0:3]
	#set yrange [0:30]

	set title "variables->secs $SOLVER"
	set output "plot-variables-secs-$SOLVER.png"
	plot "data.txt" using $FVARIABLES:$FSECS title "" pointtype 7 lc '#ff0000'

!


# variables -> timeouts

echo "$SOLVER variables->timeouts"

grep "^$SOLVER " random-* | \
sed 's,  *, ,g' | cut -d' ' -f2 | sort -n | uniq -c | \
sed 's,^  *,,' | sort -t' ' -k2,2 > total.txt

grep "^$SOLVER.*TIMEOUT" random-* | \
sed 's,  *, ,g' | cut -d' ' -f2 | sort -n | uniq -c | \
sed 's,^  *,,' | sort -t' ' -k2,2 > timeouts.txt

join -t' ' -j 2 timeouts.txt total.txt | sort -n > all.txt

[ -s timeouts.txt ] && \
gnuplot <<-!

	set terminal png
	set xrange [2.5:$(dc -e "$VARS 0.5 + p")]
	#set yrange [0:30]

	set title "variables->timeouts+total $SOLVER"
	set output "plot-variables-timeouts+total-$SOLVER.png"
	set boxwidth 0.5 relative
	plot "all.txt" using 1:3 title "" with boxes			\
	               linecolor '#00ff00' linewidth 3 fill pattern 5,	\
	     "all.txt" using 1:2 title "" with boxes			\
	               linecolor '#ff0000' fillstyle solid

!

[ -s timeouts.txt ] && \
gnuplot <<-!

	set terminal png
	set xrange [2.5:$(dc -e "$VARS 0.5 + p")]
	set yrange [0:100]

	set title "variables->timeouts/total $SOLVER"
	set output "plot-variables-timeouts-percentage-$SOLVER.png"
	set boxwidth 0.5 relative
        plot "all.txt" using (\$1):(\$2/\$3*100) title "" with lines \
	               linecolor '#ff0000' linewidth 3

!


# forget / variables -> timeouts

echo "$SOLVER forget/variables->timeouts"

grep "^$SOLVER.*TIMEOUT" random-* | \
sed 's,  *, ,g' | cut -d' ' -f2,3 | \
awk '{ printf("%0.1g\n", $2/$1) }' | sort -n | uniq -c > timeouts.txt

[ -s timeouts.txt ] && \
gnuplot <<-!

	set terminal png
	set xrange [-0.05:1.05]
	#set yrange [0:30]

	set title "forget/variables->timeouts $SOLVER"
	set output "plot-forget-variables-timeouts-$SOLVER.png"
	set boxwidth 0.5 relative
	set xtics 0.1
	plot "timeouts.txt" using 2:1 title "" pointtype 7 lc '#ff0000' \
	with boxes fillstyle solid

!


# variables -> kb (real memory)

echo "$SOLVER variables->kb"

gnuplot <<-!

	set terminal png
	#set xrange [0:3]
	#set yrange [0:30]

	set title "variables->kb $SOLVER"
	set output "plot-variables-kb-$SOLVER.png"
	plot "data.txt" using $FVARIABLES:$FKB title "" pointtype 7 lc '#ff0000'

!


# clauses -> output (real size)

echo "$SOLVER clauses->size"

grep "^$SOLVER " random-* | \
grep -v TIMEOUT > data.txt
# sed 's,TIMEOUT,10000,g' > data.txt

gnuplot <<-!

	set terminal png
	#set xrange [0:3]
	#set yrange [0:30]

	set title "clauses->size $SOLVER"
	set output "plot-clauses-size-$SOLVER.png"
	plot "data.txt" using $FCLAUSES:$FSIZE title "" pointtype 7 lc '#ff0000'

!


# clauses -> time

for FORGET in $(seq 1 $VARS);
do
	echo "$SOLVER clauses->time forget=$FORGET"

	grep "^$SOLVER " random-$VARS-$FORGET-* | \
	sed 's,TIMEOUT$,10.0,g' > data.txt

	gnuplot <<-!

		set terminal png
		#set xrange [0:3]
		#set yrange [0:30]

		set title "clauses->time $SOLVER vars=$VARS forget=$FORGET"
		set output "plot-clauses-time-$SOLVER-$VARS-$FORGET-+.png"
		plot "data.txt" using $FCLAUSES:$FTIME title "" pointtype 7 lc '#ff0000'

	!

done


# forget -> time

for CLAUSES in $(ls random-$VARS-* | cut -d- -f4 | cut -d. -f1 | sort -u);
do
	echo "$SOLVER forget->time clauses=$CLAUSES"

	grep "^$SOLVER " random-$VARS-*-$CLAUSES.* | \
	sed 's,TIMEOUT$,10.0,g' > data.txt

	C=$(printf '%02d' $CLAUSES)

	gnuplot <<-!

		set terminal png
		#set xrange [0:3]
		#set yrange [0:10]

		set title "forget->time $SOLVER vars=$VARS clauses=$CLAUSES"
		set output "plot-forget-time-$SOLVER-$VARS-+-$C.png"
		plot "data.txt" using $FFORGET:$FTIME title "" pointtype 7 lc '#ff0000'

	!

done


# clauses -> memory

for FORGET in $(seq 1 $VARS);
do
	echo "$SOLVER clauses->time forget=$FORGET"

	grep "^$SOLVER " random-$VARS-$FORGET-* | \
	sed 's,TIMEOUT$,10.0,g' > data.txt

	gnuplot <<-!

		set terminal png
		#set xrange [0:3]
		#set yrange [0:30]

		set title "clauses->memory $SOLVER vars=$VARS forget=$FORGET"
		set output "plot-clauses-memory-$SOLVER-$VARS-$FORGET-+.png"
		plot "data.txt" using $FCLAUSES:$FMEMORY title "" pointtype 7 lc '#ff0000'

	!

done


# forget -> memory

for CLAUSES in $(ls random-$VARS-* | cut -d- -f4 | cut -d. -f1 | sort -u);
do
	echo "$SOLVER forget->time clauses=$CLAUSES"

	grep "^$SOLVER " random-$VARS-*-$CLAUSES.* | \
	sed 's,TIMEOUT$,10.0,g' > data.txt

	C=$(printf '%02d' $CLAUSES)

	gnuplot <<-!

		set terminal png
		#set xrange [0:3]
		#set yrange [0:10]

		set title "forget->memory $SOLVER vars=$VARS clauses=$CLAUSES"
		set output "plot-forget-memory-$SOLVER-$VARS-+-$C.png"
		plot "data.txt" using $FFORGET:$FMEMORY title "" pointtype 7 lc '#ff0000'

	!

done


# forget -> timeouts

for CLAUSES in $(ls random-$VARS-* | cut -d- -f4 | cut -d. -f1 | sort -u);
do

	echo "$SOLVER forget->timeouts clauses=$CLAUSES"

	grep "^$SOLVER.*TIMEOUT" random-$VARS-*-$CLAUSES.* | \
	sed 's,  *, ,g' | cut -d' ' -f3 | sort -n | uniq -c > timeouts.txt

	[ -s timeouts.txt ] || continue
	echo "$SOLVER forget->timeouts clauses=$CLAUSES"

	C=$(printf '%02d' $CLAUSES)

	gnuplot <<-!

		set terminal png
		set xrange [3:10]
		#set yrange [0:10]

		set title "forget->timeouts $SOLVER vars=$VARS clauses=$CLAUSES"
		set output "plot-forget-timeouts-$SOLVER-$VARS-+-$C.png"
		plot "timeouts.txt" using 2:1 title "" pointtype 7 lc '#ff0000'

	!

done


# end loop on solvers

done


# cd back

cd -
