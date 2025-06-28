# Containernet Decision Tree

This project demonstrates how to integrate a decision tree classifier with Containernet. The system divides a trained decision tree into subtrees, deploys them as separate Docker containers in a Containernet topology, and allows inference requests to flow through the network. Each container runs a Flask server that processes its partition of the tree and forwards the request as needed. The setup includes configuration files, a Dockerfile, and a Makefile to simplify building, running, and testing the system.

## Features

* Decision tree served across multiple containers
* Containernet-based emulated network topology
* Flask-based HTTP API for inference
* Makefile for building, running, and cleaning the environment
* Example client script to send test data

## How to use

1. Build the Docker image:

   ```
   make build
   ```

2. Start the Containernet topology and servers:

   ```
   make run
   ```

3. Send a test request to the first partition:

   ```
   make client
   ```

4. Clean up the network and containers:

   ```
   make clean
   ```

## Requirements

* Ubuntu 22.04 or newer
* Docker and Containernet installed
* Python 3.9+ for container image
* Dependencies listed in `requirements.txt` (though I personally feel some could be missing)

## Architecture for reference

```
[Client]
   |
   | HTTP POST /infer
   v
+----------+       +----------+       +----------+
|  d1      | ----> |  d2      | ----> |  d3      |
| partition|       | partition|       | partition|
|   0      |       |   1      |       |   2      |
+----------+       +----------+       +----------+
        Containernet virtual switch links

```
