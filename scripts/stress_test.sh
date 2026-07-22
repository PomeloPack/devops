#!/bin/bash
echo "stress test run"
echo "CTRL+C pro kill"

# loop cyklus
for i in {1..20}; do
    
    while true; do
        curl -s http://localhost:5500/ > /dev/null
        curl -s http://localhost:5500/cities > /dev/null
        curl -s http://localhost:5500/health > /dev/null
    done &
done

# ctrlc na kill jinak to furt pojede
wait