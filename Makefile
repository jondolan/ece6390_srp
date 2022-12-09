USER:=$(shell id -u)
GROUP:=$(shell id -g)

run:
	docker run -it -v ${PWD}:/run ece6390

open:
	docker run -it --user=${USER}:${GROUP} -v ${PWD}:/run --entrypoint=/bin/bash ece6390

build:
	docker build -t ece6390 .
