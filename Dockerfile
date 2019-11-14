FROM continuumio/miniconda3
ARG CONDA_ENV=mentorpal
ENV MENTORPAL_CONDA_ENV=mentorpal
RUN conda create --name=${MENTORPAL_CONDA_ENV} python=3.6 pip
RUN echo "source activate ${MENTORPAL_CONDA_ENV}" > ~/.bashrc
ENV PATH /opt/conda/envs/${MENTORPAL_CONDA_ENV}/bin:$PATH
COPY . /tmp/mentorpal-classifiers
RUN bash -c "source activate ${MENTORPAL_CONDA_ENV} && \
    pip install /tmp/mentorpal-classifiers" \
    && rm -rf /tmp/bin
COPY ./bin /tmp/bin
RUN bash -c "source activate ${MENTORPAL_CONDA_ENV} \
    && python /tmp/bin/nltk_setup.py" \
    && rm -rf /tmp/bin
