---
layout:     post
title:      "A Love Letter to Makefiles"
date:       2021-10-10 16:26:36 +11:00
categories: tag
description: |
  A collection of things that make Makefiles great, but not necessarily for its original purpose...
---

The first time I was introduced to Makefiles was working on a rather large
computational chemistry simulation software, written in Fortran 95. This was not
a complex piece of software from a system architecture perspective: it reads
a bunch of text files as input, then outputs a deluge of numbers to stdout while
occupying 100% of all the CPUs it's allowed to touch.

Almost like a crypto-mining application.

My first thought, looking at the bizarre syntax in Makefiles, was an appreciation
of how Microsoft's Visual Studio manages the project build all through a nice UI.
That's how life should be, this "makefile" business is so very ghetto.

As we worked on this application, and others like this (a mixture of C and python),
makefiles began to grow on us. We would begin to put convenience actions such as
running local tests, publishing binaries, even deploying to remote supercomputers.

Years later, I'd learn that what we did was "CI/CD in the cloud".

## Who still use Fortran and C anyway?

Yes, a big part of the makefile is to manage build dependencies, and more importantly
to know what code hasn't changed and therefore doesn't need re-building.
A well-setup makefile would speed up development and test significantly.

<center>
<img src="https://imgs.xkcd.com/comics/compiling.png"><br/>

Relevant <a href="https://xkcd.com/303/">xkcd</a> from 2007...
</center>

Compilation dependency is hardly the concern for most of us in 2021. We live in a world of
docker, maven, webpack, etc... Even unorthodox uses of makefiles for CI/CD steps
have to contend with terraform, terragrunt, the various cloud vendor CLIs...

Everything has their own CLIs. Surely the days of Makefiles are over?

## A human brain and scratch space

- Brains run out of space
- Things get really slow
- Surely there's a better way?

## A wild Jenkins appears

- Put steps into CI
- Migrate to other CI??

## Let's make a wishlist for a custom CLI

- Self-documenting: we should be able to add some description/words for each action
- Linux-native: we should be able to run it on a standard CI worker, docker image or local laptop
- Input variables
- Colourful
- Easy enough to read

Some use-cases:
- Run a monitoring/status script
- Start/stop a long-running service without dealing with systemd
- Run a local web server
- Run some AWS commands that require a json file as input
- Build something and push to AWS

## A sample makefile

```
_GREEN='\033[0;32m'
_YELLOW='\033[0;33m'
_RED='\033[0;31m'
_RESET='\033[0m'

# sets makefile to use bash, rather than the default sh
SHELL=/bin/bash
# run login profiles, respect .bashrc, fail on error
.SHELLFLAGS=-lec
# commands run consecutively in the same shell, variables can persist
.ONESHELL:

# never skip any make targets, effectively disables "change detection"
.PHONY: $(MAKECMDGOALS)


help:					## # Show this help
	@echo "Usage:"
	@sed -ne '/@sed/!s/:.*## / /p' $(MAKEFILE_LIST) \
		| sed 's/^/  make /' \
		| column -s "#" -t


cmd_w_var:				## MYVAR=<value>  # run a command with MYVAR
ifndef MYVAR
	$(error MYVAR is undefined, check `make help` to see usage)
endif
	some_cmd --var=${MYVAR}


cmd_w_tmp_file:			## # run a command that needs a small config file (looking at you awscli), heredoc is very handy here
	cat <<- EOF > /tmp/foobar.json
	{
		"foo": [
			"bar"
		]
	}
	EOF
	some_cmd --file /tmp/foobar.json


cmd_w_log:				## # run a script and capture output with timestamp
	bash my_script.sh 2>&1 \
		| ts '[%Y-%m-%d %H:%M:%S]' \
		>> my_script.log


crontab:				## # put something into crontab, like a command with logging
	crontab -l \
		| grep -v "make cmd_w_log" \
		| { cat; echo '*/10 * * * * bash -c "cd $(PWD) && make cmd_w_log"'; } \
		| crontab -


aussie:					## # print straya colours
	@echo -e ${_GREEN}AUSSIE AUSSIE AUSSIE ${_YELLOW}OI OI OI${_RESET}

```

The help from above makefile renders using regex `<target>: ## <var> # <txt>`.
```
Usage:
  make help                        Show this help
  make cmd_w_var MYVAR=<value>     run a command with MYVAR
  make cmd_w_tmp_file              run a command that needs a small config file (looking at you awscli), heredoc is very handy here
  make cmd_w_log                   run a script and capture output with timestamp
  make crontab                     put something into crontab, like a command with logging
  make aussie                      print straya colours
```


## It's dangerous out there, take this!

- When steps get too large, put them in a bash script in another folder. Avoid 2k lines in a makefile.
- Avoid sudo in a makefile if you can. They really shouldn't be part of your build!
- Avoid secrets!
