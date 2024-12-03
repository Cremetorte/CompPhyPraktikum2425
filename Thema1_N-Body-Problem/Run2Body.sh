for i in euler euler-cromer velocity_verlet RK4 heun hermite hermite_it; do 
    for delta in 0.5 0.1 0.05 0.01; do
        # ./nbody.py --integrator $i --input_file 2body --output_file 2body.$i.$delta -t $delta --endtime 6.283185307179586 -v ;
        ./nbody_simulation $i 2 $delta 15.7 false
    done
done
cd /Output/2-body
for delta in 0.5 0.1 0.05 0.01; do
    # ./nbody.py --integrator $i --input_file 2body --output_file 2body.$i.$delta -t $delta --endtime 6.283185307179586 -v ;
    python3 2BodyProcessor.py $delta
done