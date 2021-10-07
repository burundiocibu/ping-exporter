# ping-exporter
A Prometheus exporter for ping responses. This is an experiment to see of 
logging the data in a way that plays nicely with prometheus works
better than just logging min/mean/max/std/loss

pipenv install --dev
 
 - or -

docker build -t ping-exporter .