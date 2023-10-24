# First load the numpy-mp container
FROM clearlinux/numpy-mp@sha256:cc0250d7e2832859a855fed0be478340b4b9e478cd136487d2601e6cdecc626f
LABEL maintainer="Mathys Grapotte" \
        name="alessiovignoli3/model-check:generate_fasta" \
        description="Docker image containing python packages required for generating fastas in the model-check pipeline"

# installing the python jaspar API from pip
RUN pip install pyjaspar==3.0.0

