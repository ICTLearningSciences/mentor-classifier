FROM continuumio/miniconda3
ARG CONDA_ENV=mentor
ENV mentor_CONDA_ENV=mentor
RUN conda create --name=${mentor_CONDA_ENV} python=3.6 pip
RUN echo "source activate ${mentor_CONDA_ENV}" > ~/.bashrc
ENV PATH /opt/conda/envs/${mentor_CONDA_ENV}/bin:$PATH
COPY . /tmp/mentor-classifiers
RUN bash -c "source activate ${mentor_CONDA_ENV} && \
    pip install /tmp/mentor-classifiers" \
    && rm -rf /tmp/bin
COPY ./bin /tmp/bin
RUN bash -c "source activate ${mentor_CONDA_ENV} \
    && python /tmp/bin/nltk_setup.py" \
    && rm -rf /tmp/bin
