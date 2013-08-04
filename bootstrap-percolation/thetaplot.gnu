#! /usr/bin/gnuplot
set terminal png transparent nocrop enhanced font arial 8 size 420,320 
set key bmargin left horizontal Right noreverse enhanced autotitles box linetype -1 
set output 'results1.png'
plot 1 - exp(-x),'theta1data'
set output 'results2.png'
plot 1 - (1+x)*exp(-x),'theta2data'
set output 'results3.png'
plot 1 - exp(-x**2), 'theta3data'
set output 'results4.png'
plot 1 - 2*exp(-x**2/2) + exp(-x**2), 'theta4data'
set output 'results5.png'
plot 1 - exp(-x**3/3),'theta5data'
set output 'results6.png'
plot 1 - 2*exp(-x**3/6) + exp(-x**3/3),'theta6data'
set output 'results7.png'
plot 1 - exp(-x**4/12),'theta7data'
set output 'results8.png'
plot 1 - 2*exp(-x**4/24) + exp(-x**4/12),'theta8data'
