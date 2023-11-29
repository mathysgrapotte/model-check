#Python 3.10 slim-bullseye
FROM python@sha256:9b009a025fa0c270a1617086d74bde1f7015fdcb8a8447aca14ec0de78d99f74
LABEL maintainer="Alessio Vignoli" \
    name="alessiovignoli3/model-check:pwm2homer" \
	description="Docker image containing python packages required for model-check pipeline, from jaspar matrix to homer format"

# installing python needed packages
RUN pip install \
	pandas==2.1.3 \
    bio==1.6.0 \
    numpy==1.26.2
