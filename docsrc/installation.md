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

If you want GPU support you will need to install NVIDIA Container Toolkit from: <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html> and Docker >= _19.03_

```
docker run --gpus all -v $(pwd):/app/Probe-Ably/configurations -p 8031:8031 -it aisystems/probe-ably bash
```

The Docker container exposes `/app/Probe-Ably/configurations` volume for external data facilitating the load of configurations file along with `8031` port.
