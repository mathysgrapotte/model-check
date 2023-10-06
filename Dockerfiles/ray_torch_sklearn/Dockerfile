# Use clear linux multiprocessing numpy container as a base
#FROM alpine@sha256:48d9183eb12a05c99bcc0bf44a003607b8e941e1d4f41f9ad12bdcc4b5672f86
FROM python@sha256:e170f5079a2514ff79ab85a4af229351a979531c8d4cedeaeed2901eaaa6c177
LABEL maintainer="Alessio Vignoli" \
        name="alessiovignoli3/model-check:dataload_training" \
        description="Docker image containing python packages required for model-check pipeline"

# installing python needed packages
RUN pip install \
		torch==2.1.0 \
		ray==2.3.0 \
		ray[rllib] \
        scipy==1.11.3 \ 
		scikit-learn==1.3.1 \
		pandas==2.1.1
