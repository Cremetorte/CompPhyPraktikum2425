for i in hermite hermite_it; do 
    for delta in 0.5 0.1 0.05 0.01; do
        for N in 100 1000; do
            ./nbody_simulation $i $N $delta 6.3 false
        done
    done
done