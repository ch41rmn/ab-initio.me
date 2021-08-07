run:
	bundle exec jekyll serve --force-polling

png2base64:
	@echo -n '<img src="data:image/png;base64,' \
		&& cat $(IMAGE) | base64 -w 0 \
		&& echo '"/>'

