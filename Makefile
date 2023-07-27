.PHONY: build

build:
	sam build

deploy-infra:
	sam build && sam deploy --no-confirm-changeset --no-fail-on-empty-changeset

deploy-site:
	aws s3 sync ./resume-site s3://www.clouddanny.net

invoke-local:
	sam build && sam local invoke ResumeFunction

invoke-remote:
	sam build && sam remote invoke ResumeFunction