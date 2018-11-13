GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

#Change projectname before building
#(projectname should have no underscore or spaces and be lowercase)
PROJECT_NAME=agile
BUCKET_NAME=kubernetes-django-agile
SQL_CONNECTION_NAME=kubernetes-222111:europe-west4:agile

.PHONY: push
push: build
	docker push eu.gcr.io/$(GCLOUD_PROJECT)/$(PROJECT_NAME)

.PHONY: build
build:
	docker build -t eu.gcr.io/$(GCLOUD_PROJECT)/$(PROJECT_NAME) .

.PHONY: template
template:
	sed -i ".tmpl" "s/\$$GCLOUD_PROJECT/$(GCLOUD_PROJECT)/g" agile.yaml

#In deployment projectname must consist of lowercase name without underscore
.PHONY: deploy
deploy:
	kubectl run $(PROJECT_NAME) --image eu.gcr.io/$(GCLOUD_PROJECT)/$(PROJECT_NAME) --port 8080

# .PHONY: expose
# expose:
# 	kubectl expose deployment $(PROJECT_NAME) --type LoadBalancer --port 80 --target-port 8080

.PHONY: update
update:
	kubectl set image deployment $(PROJECT_NAME) $(PROJECT_NAME)-app=eu.gcr.io/$(GCLOUD_PROJECT)/$(PROJECT_NAME):$(version)

.PHONY: syncstatic
syncstatic:
	gsutil rsync -R static/ gs://$(BUCKET_NAME)/static

.PHONY: delete
delete:
	kubectl delete rc agile
	kubectl delete service agile


#TODO create a nice make target for serving
#docker run --name empty_kubernetes -d -p 80:8080 eu.gcr.io/kubernetes-222111/empty-kubernetes
