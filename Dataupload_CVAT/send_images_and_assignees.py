import os
from cvat_sdk import make_client
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


# Assignees and their task limits
assignees = {
    "assignee_1": 10,
    "assignee_2": 10,
    "assignee_3": 10,
    "assignee_4": 10
}

# Get the list of folders
folders = [os.path.join(images_folder, folder) for folder in os.listdir(images_folder)]

# Create a Client instance bound to a local server and authenticate using basic auth
with make_client(host=host, credentials=(username, password)) as client:
    # Set the organization context
    client.organization_slug = slug
    
    # Retrieve project details
    project = client.projects.retrieve(project_id)
    
    # Check if the project is in the correct organization
    if hasattr(project, 'organization'):
        raise ValueError(f"Project {project_id} is not in organization {slug}.")
    
    # Retrieve the user IDs of the assignees
    users = client.users.list()
    assignee_ids = {user.username: user.id for user in users if user.username in assignees}
    
    if len(assignee_ids) != len(assignees):
        missing_users = set(assignees) - set(assignee_ids)
        raise ValueError(f"Users {', '.join(missing_users)} not found.")
    
    task_counter = {username: 1 for username in assignees}
    
    for i, folder in enumerate(folders):
        task_name = f"{task_preset}_{start_task_id}"
        start_task_id += 1
        
        # Get the list of images in the current folder
        image_files = [os.path.join(folder, image) for image in os.listdir(folder)]

        # Create a task using the task repository method
        try:
            for username, limit in assignees.items():
                if task_counter[username] < limit:
                    # Fill in task parameters with assignee
                    task_spec = {
                        "name": task_name,
                        "project_id": project_id,
                        "assignee_id": assignee_ids[username]
                    }

                    task = client.tasks.create_from_data(
                        spec=task_spec,
                        resource_type=ResourceType.LOCAL,
                        resources=image_files,
                    )
                    print(f"Task {task_name} created successfully with ID {task.id} and assigned to user {username}.")
                    task_counter[username] += 1
                    break
        except Exception as e:
            print(f"Exception when creating or assigning task {task_name}: {e}")
