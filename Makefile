all: index.html urp.1.html

index.html: index.md
	pandoc -s -t html5 $< -o $@

.INTERMEDIATE: urp.1.ronn
urp.1.html: urp.1.ronn
	ronn --html --style=toc $<

urp.1.ronn:
	wget https://raw.githubusercontent.com/jdp/urp/master/man/urp.1.ronn -O $@

clean:
	-rm index.html urp.1.html

.PHONY: all clean
