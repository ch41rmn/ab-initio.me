DATETIME := $(shell date --rfc-3339=second | sed 's/+/ +/g' )
DATE := $(shell date --iso-8601 )

_GREEN="\033[0;32m"
_YELLOW="\033[0;33m"
_RED="\033[0;31m"
_RESET="\033[0m"

SHELL=/bin/bash
.SHELLFLAGS=-lc
.ONESHELL:

.PHONY: all $(MAKECMDGOALS)

help:			## # Show this help
	@echo "Usage:"
	@sed -ne '/@sed/!s/:.*## / /p' $(MAKEFILE_LIST) \
		| sed 's/^/  make /' \
		| column -s "#" -t

run:			## # Run Jekyll site locally
	bundle exec jekyll serve --force-polling

png2base64:		## IMAGE=<path> # Convert PNG image to an embedded base64 img tag
ifndef IMAGE
	$(error IMAGE is undefined, check `make help` to see usage)
endif
	@echo -n '<img src="data:image/png;base64,' \
		&& cat $(IMAGE) | base64 -w 0 \
		&& echo '"/>'

new:			## # Create a new post with today's date
	(\
		echo "---" \
		&& echo "layout:     post" \
		&& echo 'title:      "Title"' \
		&& echo 'date:       $(DATETIME)' \
		&& echo 'categories: tag' \
		&& echo 'description: |' \
		&& echo '  Description' \
		&& echo '---' \
	) > _posts/$(DATE)-post.md
