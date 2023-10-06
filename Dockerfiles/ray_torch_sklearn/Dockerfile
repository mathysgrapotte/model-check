# Use clear linux multiprocessing numpy container as a base
FROM pytorch/torchserve@sha256:23b0b49e9ec240085c046a918fb7a5f9af58e6ee93107689269b36edcf4aca18
LABEL maintainer="Alessio Vignoli" \
        name="alessiovignoli3/model-check:dataload_training" \
        description="Docker image containing python packages required for model-check pipeline"

RUN pip install \
		ray==2.3.0 \
		ray[rllib] \
        scipy==1.11.3 \ 
		scikit-learn==1.3.1 \
		pandas==2.1.1
