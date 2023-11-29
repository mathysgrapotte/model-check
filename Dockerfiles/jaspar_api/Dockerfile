#Python 3.10 slim-bullseye
FROM python@sha256:9b009a025fa0c270a1617086d74bde1f7015fdcb8a8447aca14ec0de78d99f74
LABEL maintainer="Alessio Vignoli" \
    name="alessiovignoli3/model-check:jaspar_api" \
	description="Docker image containing python packages required for model-check pipeline, jaspar matrix download"

# installing python needed packages
RUN pip install \
	coreapi-cli==1.0.9
