DATETIME := $(shell date --rfc-3339=second | sed 's/+/ +/g' )
DATE := $(shell date --iso-8601 )

run:
	bundle exec jekyll serve --force-polling

png2base64:
	@echo -n '<img src="data:image/png;base64,' \
		&& cat $(IMAGE) | base64 -w 0 \
		&& echo '"/>'

new:
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
