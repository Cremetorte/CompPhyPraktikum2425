for z in 0.56, 0.84; do
    # run all z in parallel
    ./gcmc $z false & 
done