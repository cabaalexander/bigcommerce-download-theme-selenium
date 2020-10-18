# vim: ts=4:sw=4

project_folder	?=

download:
	@pipenv run start

extract:
	@./extract-config.sh $(project_folder)

.PHONY: download extract
