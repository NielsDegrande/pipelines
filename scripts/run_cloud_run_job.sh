#!/bin/bash

# Stop upon error and undefined variables.
# Print commands before executing.
set -eux

# Variables for substitution in the YAML file.
export PROJECT_ID=''
export REGION=''
export JOB_NAME=''
export PIPELINE_NAME=''
export EXAMPLE=''
export IMAGE=''
export CLOUDSQL_INSTANCE=''

##########
#  ONCE  #
##########

# Authenticate to Google Cloud (if needed).
gcloud auth login
# Set the project ID.
gcloud config set project "$PROJECT_ID"

# Deploy the container to Cloud Run with environment variables.
# Reading the YAML file and replacing placeholders.
gcloud run jobs replace <(envsubst <scripts/pipeline_job.yaml) --region "$REGION"

###############
#  RECURRING  #
###############

gcloud run jobs execute "$JOB_NAME" --region "$REGION"
