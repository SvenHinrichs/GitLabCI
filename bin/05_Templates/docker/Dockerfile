FROM ubuntu:18.04
# Avoid warnings
# debconf: unable to initialize frontend: Dialog
# debconf: (TERM is not set, so the dialog frontend is not usable.)

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update 
RUN apt-get upgrade -y		

RUN apt-get --no-install-recommends install -y\
  x11-apps \
  g++-4.8 \
  git \
  unzip \
  zip=3.* \
  rpm \
  tidy \
  alien \
  lsb \
  sudo \
  python3.6 \
  x11vnc \
  libglu1-mesa:amd64=9.0.* \
  libjpeg62-dev \
  libc6-i386\
  g++-multilib \
  libxcomposite-dev \
  libxi6 \ 
  libasound2 \
  dbus \
  libegl1 \
  xvfb \
  curl \
  python-pip && \
  rm -rf /var/lib/apt/lists/*
ENV LANG C.UTF-8
ENV PYTHONIOENCODING UTF-8
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
RUN conda create -n python36 python=3.6 -y
RUN ["/bin/bash", "-c", "source activate python36 && conda install numpy scipy matplotlib -y" ]
RUN ["/bin/bash", "-c", "source activate python36 && pip install git+https://github.com/lbl-srg/BuildingsPy@master" ]
RUN echo "===Installation successful"


