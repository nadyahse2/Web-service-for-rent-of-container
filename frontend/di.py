import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:5000"

@st.cache_data
def get_default_image():
    return "ubuntu"

@st.cache_data
def get_default_mem_limit():
    return "512m"

@st.cache_data
def get_default_cpu_limit():
    return 1.0

def create_container(image, mem_limit, cpus):
    try:
        payload = {"image": image, "mem_limit": mem_limit, "cpus": cpus}
        response = requests.post(f"{BACKEND_URL}/containers", json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        st.session_state.container_id = data['id'] #storing to do action on container

        st.success(f"Container created! ID: {data['id']}, SSH Port: {data['ssh_port']}, IP Address: {data['ip_address']}")
        st.info(f"To connect via SSH, use IP: {data['ip_address']} and Port: {data['ssh_port']}") # Show connection info

    except requests.exceptions.RequestException as e:
        try:
            error_message = response.json()['error']
        except:
            error_message = str(e)
        st.error(f"Error creating container: {error_message}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def start_container(container_id):
    try:
        response = requests.post(f"{BACKEND_URL}/containers/{container_id}/start")
        response.raise_for_status()
        data = response.json()
        st.success(f"{data['message']}")
    except requests.exceptions.RequestException as e:
        try:
            error_message = response.json()['error']
        except:
            error_message = str(e)
        st.error(f"Error starting container: {error_message}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def stop_container(container_id):
    try:
        response = requests.post(f"{BACKEND_URL}/containers/{container_id}/stop")
        response.raise_for_status()
        data = response.json()
        st.success(f"{data['message']}")
    except requests.exceptions.RequestException as e:
        try:
            error_message = response.json()['error']
        except:
            error_message = str(e)
        st.error(f"Error stopping container: {error_message}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def remove_container(container_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/containers/{container_id}")
        response.raise_for_status()
        data = response.json()
        st.success(f"{data['message']}")
        st.session_state.container_id = None #Clean from memory
    except requests.exceptions.RequestException as e:
        try:
            error_message = response.json()['error']
        except:
            error_message = str(e)
        st.error(f"Error removing container: {error_message}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.title("Docker Container Manager")

st.header("Create Container")
image = st.text_input("Image Name", value = get_default_image())

mem_limit = st.text_input("Memory Limit", value = get_default_mem_limit())
cpus = st.number_input("CPU Limit", min_value=0.1, max_value=4.0, step=0.1, value = get_default_cpu_limit())

if st.button("Create Container"):
    create_container(image, mem_limit, cpus)

if 'container_id' in st.session_state: #checking is there any container to action on it
    container_id = st.session_state.container_id

    st.header("Manage Container")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start Container"):
            start_container(container_id)
    with col2:
        if st.button("Stop Container"):
            stop_container(container_id)
    with col3:
        if st.button("Remove Container"):
            remove_container(container_id)
else:
    st.write("No container created yet.")