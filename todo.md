The enviroment files goes like this, we select one from the "host" dir for example: "/host/iardo-vps-iardodev/.env", this file is to provide some env variables depending on host configuration mainly ports and some global values, then every host has a stack of services to install, depending on the services ut wants to install also loads .envs inside de "/serv" dir for each service, now my question is, how do i create an override system that is secure to also depending on the host override things like sectrets and user/pass combinations for the services? and that is compatible with komodo

TODO: Create claude skills hardness for better code output;

TODO: Make and audit in all the repo to check for security issues

TODO: I have a bunch of host that are unreachable for komodo, i want to know is there a way to ignore the from the komodo config so the do not show up in the UI as failed but keeping my files intact

TODO: Create a documentation on how the process works, theres two ways to install services of this repo, via the ./start.py or using komodo, normally the when i clone this repo the first time i will use the ./start.py using one of the host to install komodo then from there on out i use komodo to deploy stacks to other machines, but komodo is optional we can install any host stack with ./start.py. Make the explanation in the documentation short, concise, use layman-terms, if a line ends with dot or comma please break line. Make this docs to be redable for anyone of for myself in the future assuming im going to forget how most of this works.
