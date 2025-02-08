for z in 0.05, 0.125, 0.25, 0.56, 0.84, 1.1, 1.15, 1.5; do
    # run all z in parallel
    ./gcmc $z false & 
done