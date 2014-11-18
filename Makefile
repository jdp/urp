all: man/urp.1 man/urp.1.html

man/urp.1: man/urp.1.ronn
	ronn --roff $<

man/urp.1.html: man/urp.1.ronn
	ronn --html --style=toc $<

.PHONY: all
