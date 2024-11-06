# Makefile to run Python script and generate directory structure in index.json, index.html, and index.xml

# Target to run the Python script and generate index.json, index.html, and index.xml in the current directory
.PHONY: generate

generate:
	@echo "Generating directory structure files as index.json, index.html, and index.xml..."
	python3 index.py

# Clean target to remove the generated JSON, HTML, and XML files in the current directory
.PHONY: clean

clean:
	@echo "Removing generated files index.json, index.html, and index.xml..."
	rm -f index.json index.html index.xml

# Serve target to start an HTTP server from the current directory, running clean and generate before serving
.PHONY: serve

serve:
	python3 -m http.server --directory .

lint:
	npm install --save-dev prettier
	npx prettier --write index.html index.json
