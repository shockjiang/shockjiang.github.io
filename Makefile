
build:
	python3 _build.py

start:
	cd _site && python3 -m http.server 4000

clean:
	rm -rf _site
