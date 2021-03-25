# Installation

## Pre-Requisites

The following dependencies need to be pre-installed in-order for the application to be run:

- `yarn` >= 1.16.0 ([Install instructions](https://classic.yarnpkg.com/en/docs/install/))
- `pip` >= 20.0.2 ([Install instructions](https://pip.pypa.io/en/stable/installing/))

## Installing Probe-Ably

For Users:

```
git clone https://github.com/ai-systems/Probe-Ably.git
pip install -r requirements.txt
cd probe_ably/service
yarn install
yarn build
```

For developers:

Run the following additional command

```
pip install -r requirements-dev.txt
```

## Using Docker Image

You will additionally need to install NVIDIA-Docker (https://github.com/NVIDIA/nvidia-docker) if you want GPU support else you can use the following commands with vanilla docker.

```
nvidia-docker run -v $(pwd)/tests:/app/Probe-Ably/configurations -p 8031:8031 -it probe-ably bash
```
