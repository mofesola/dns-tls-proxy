#DNS Over TLS with TCP and UDP listeners

This project embeds a python script deployed with docker to listen for DNS requests on both TCP and UDP ports 53, and
forwards it over a secure TLS connection to a TLS enabled DNS upstream server. The python script uses processes and threads.
One process for each protocol and as many threads as possible will be started per process, based on incoming requests.
I have tested one deployment of this service with 10 concurrent DNS requests on both TCP and UDP and it works just fine

There exists a `docker-compose.yml` file to enable a quick launch of the application. 
Just run `docker-compose up --build -d` to run this in detached mode and start listening for DNS requests

##Security concerns of using a DNS proxy:
While it's true that encrypting your DNS requests gives you an additional layer of security, there are a number of
issues that could pose a security risk
* The proxy could be attacked and DNS requests or responses read, or altered
* Security, patching and upgrade of this service becomes ours to work on, and should be done reliably

##Microservice design
This service should be deployed with multiple instances behind a loadbalancer. The containers should be self healing,
and should any container go down, the orchestration service should bring it up again. The service should also be able to
autoscale to meet the workload demand. Since each request processes in milliseconds, a round-robin loadbalancing algorithm
may be preferred in this use case.

##ToDo
* Generate and use a proper TLS cert for the handshake
* Create additional setup to make it easy to deploy at scale, on Kubernetes, for example.
* Take IPv6 requests
* Split each protocol into different classes
* Better documentation
