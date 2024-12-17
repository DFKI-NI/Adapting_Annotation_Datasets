import os
from cvat_sdk import make_client, models
from cvat_sdk.core.proxies.tasks import ResourceType


# Function to read .env file and set environment variables
def load_env_file(file_path):
    """Loads and reads env file

    Args:
        file_path (str): file name for the env file
    """
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


# Load environment variables from .env file
load_env_file('./.env')

# how should your tasks be named: "{my_task_name}_{task_id}"
task_preset = "my_task_name"
start_task_id = 0

# Configuration
images_folder = "./images" # folder where your subfolders for uploading are placed
username = str(os.getenv('username'))
password = str(os.getenv('password'))
host = "cvat_ip:port" # Set your CVAT IP and Port here

project_id = 20  # Replace with your actual project ID
slug = "project_slug"

# Get the list of folders
folders = [os.path.join(images_folder, folder) for folder in os.listdir(images_folder)]

# Create a Client instance bound to a local server and authenticate using basic auth
with make_client(host=host, credentials=(username, password)) as client:
    # Set the organization context
    client.organization_slug = slug

    # Retrieve project details
    project = client.projects.retrieve(project_id)

    for i, folder in enumerate(folders):
        task_name = f"{task_preset}_{start_task_id}"
        start_task_id += 1

        # Fill in task parameters
        task_spec = {
            "name": task_name,
            "project_id": project_id
        }

        # Get the list of images in the current folder
        image_files = [os.path.join(folder, image) for image in os.listdir(folder)]

        # Create a task using the task repository method
        try:
            task = client.tasks.create_from_data(
                spec=task_spec,
                resource_type=ResourceType.LOCAL,
                resources=image_files,
            )
            print(f"Task {task_name} created successfully with ID {task.id}.")
        except Exception as e:
            print(f"Exception when creating task {task_name}: {e}")
