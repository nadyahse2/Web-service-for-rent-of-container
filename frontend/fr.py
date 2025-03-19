import streamlit as st
import requests
import json


BACKEND_URL = "http://127.0.0.1:5000"

# Docker-related functions
def create_container(image, mem_limit, cpus):
    try:
        payload = {"image": image, "mem_limit": mem_limit, "cpus": cpus}
        response = requests.post(f"{BACKEND_URL}/containers", json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        st.session_state.container_id = data['id']
        st.success(f"Container created! ID: {data['id']}, SSH Port: {data['ssh_port']}, IP Address: {data['ip_address']}")
        st.info(f"To connect via SSH, use IP: {data['ip_address']} and Port: {data['ssh_port']}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error creating container: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def start_container(container_id):
    try:
        response = requests.post(f"{BACKEND_URL}/containers/{container_id}/start")
        response.raise_for_status()
        data = response.json()
        st.success(f"Container {container_id} started: {data['message']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error starting container: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def stop_container(container_id):
    try:
        response = requests.post(f"{BACKEND_URL}/containers/{container_id}/stop")
        response.raise_for_status()
        data = response.json()
        st.success(f"Container {container_id} stopped: {data['message']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error stopping container: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def remove_container(container_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/containers/{container_id}")
        response.raise_for_status()
        data = response.json()
        st.success(f"Container {container_id} removed: {data['message']}")
        st.session_state.container_id = None  # Clear container ID from session
    except requests.exceptions.RequestException as e:
        st.error(f"Error removing container: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# VM-related functions
def create_vm(name, image, mem, cpus, disk_size):
    try:
        payload = {"name": name, "image": image, "mem": mem, "cpus": cpus, "disk_size": disk_size}
        st.write(json.dumps(payload, indent=4))
        response = requests.post(f"{BACKEND_URL}/vms", json=payload)
        response.raise_for_status()
        data = response.json()
        st.session_state.vm_name = data['name']
        st.success(f"VM created! Name: {data['name']}, Disk Path: {data['disk_path']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating VM: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def start_vm(name):
    try:
        response = requests.post(f"{BACKEND_URL}/vms/{name}/start")
        response.raise_for_status()
        data = response.json()
        st.success(f"VM {name} started: {data['message']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error starting VM: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def stop_vm(name):
    try:
        response = requests.post(f"{BACKEND_URL}/vms/{name}/stop")
        response.raise_for_status()
        data = response.json()
        st.success(f"VM {name} stopped: {data['message']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error stopping VM: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def remove_vm(name):
    try:
        response = requests.delete(f"{BACKEND_URL}/vms/{name}")
        response.raise_for_status()
        data = response.json()
        st.success(f"VM {name} removed: {data['message']}")
        st.session_state.vm_name = None  # Clear VM name from session
    except requests.exceptions.RequestException as e:
        st.error(f"Error removing VM: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Streamlit UI
st.title("Docker & VM Manager")

# Docker container section
st.header("Create Docker Container")
image = st.text_input("Docker Image Name", value="ubuntu")
mem_limit = st.text_input("Memory Limit", value="512m")
cpus = st.number_input("CPU Limit", min_value=0.1, max_value=4.0, step=0.1, value=1.0)

if st.button("Create Docker Container"):
    create_container(image, mem_limit, cpus)

# VM section
st.header("Create Virtual Machine")
vm_name = st.text_input("VM Name")
vm_image = st.text_input("VM Image", value="ubuntu")
vm_mem = st.text_input("Memory", value="512M")
vm_cpus = st.number_input("CPUs", min_value=1, max_value=16, step=1, value=2)
vm_disk_size = st.number_input("Disk Size (GB)", min_value=10, max_value=1000, step=1, value=20)

if st.button("Create Virtual Machine"):
    create_vm(vm_name, vm_image, vm_mem, vm_cpus, vm_disk_size)

# Docker management controls
if 'container_id' in st.session_state:
    container_id = st.session_state.container_id
    st.header("Manage Docker Container")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start Docker Container"):
            start_container(container_id)
    with col2:
        if st.button("Stop Docker Container"):
            stop_container(container_id)
    with col3:
        if st.button("Remove Docker Container"):
            remove_container(container_id)

# VM management controls
if 'vm_name' in st.session_state:
    vm_name = st.session_state.vm_name
    st.header("Manage Virtual Machine")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start Virtual Machine"):
            start_vm(vm_name)
    with col2:
        if st.button("Stop Virtual Machine"):
            stop_vm(vm_name)
    with col3:
        if st.button("Remove Virtual Machine"):
            remove_vm(vm_name)
