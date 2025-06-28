IMAGE = my_tree_server
PROJECT_DIR = /home/blackdragoon/containernet_project

build:
	@echo "Building Docker image..."
	sudo docker build -t $(IMAGE) $(PROJECT_DIR)

run:
	@echo "Starting Containernet topology..."
	sudo python3 $(PROJECT_DIR)/containernet_topology.py

client:
	@echo "Running client script..."
	python3 $(PROJECT_DIR)/client_script.py

clean:
	@echo "Cleaning up Docker and Mininet..."
	sudo mn -c
	- docker stop $$(docker ps -q)
	- docker rm $$(docker ps -aq)

