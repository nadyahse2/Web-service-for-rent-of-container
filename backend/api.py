from flask import Flask, request, jsonify
from docker_m import DockerManager

app = Flask(__name__)
docker_manager = DockerManager()

@app.route('/containers', methods=['POST'])
def create_container():
    try:
        data = request.get_json()
        image = data['image']
        mem_limit = data['mem_limit']
        cpus = data['cpus']

        container_id, ssh_port = docker_manager.create_container(image, mem_limit, cpus)

        if container_id:
            ip_address = docker_manager.get_container_ip(container_id)
            return jsonify({
                'id': container_id,
                'ssh_port': ssh_port,
                'ip_address': ip_address
            }), 201
        else:
            return jsonify({'error': ssh_port}), 500 #Returns error message if container_id is null

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/containers/<container_id>/start', methods=['POST'])
def start_container(container_id):
    result = docker_manager.start_container(container_id)
    if "Error" in result:
        return jsonify({'error': result}), 400
    else:
        return jsonify({'message': result}), 200

@app.route('/containers/<container_id>/stop', methods=['POST'])
def stop_container(container_id):
    result = docker_manager.stop_container(container_id)
    if "Error" in result:
        return jsonify({'error': result}), 400
    else:
        return jsonify({'message': result}), 200

@app.route('/containers/<container_id>', methods=['DELETE'])
def remove_container(container_id):
    result = docker_manager.remove_container(container_id)
    if "Error" in result:
        return jsonify({'error': result}), 400
    else:
        return jsonify({'message': result}), 200

if __name__ == '__main__':
    app.run(debug=True)

