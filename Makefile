
MD_DIR=$(shell python config.py md_dir)
HTML_DIR=$(shell python config.py html_dir)

MKD_FILES=$(shell ls $(MD_DIR)/*.md)
HTML_FILES=$(foreach path, $(MKD_FILES:.md=.html), $(HTML_DIR)/$(shell basename $(path)))

TARGET: $(HTML_FILES) index

$(HTML_DIR)/%.html: $(MD_DIR)/%.md
	./tools/make_html $< > $@

index:
	./tools/make_index > $(HTML_DIR)/index.md
	./tools/make_html $(HTML_DIR)/index.md > $(HTML_DIR)/index.html
	rm $(HTML_DIR)/index.md
	cp style.css $(HTML_DIR)

clean:
	rm -f $(HTML_FILES) $(HTML_DIR)/index.html
