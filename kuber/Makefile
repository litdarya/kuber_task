.PHONY: deploy

deploy:
	@[ "${service}" ] || (echo 'Set service name via service=...'; exit 1)
	bash run.sh $(service)
