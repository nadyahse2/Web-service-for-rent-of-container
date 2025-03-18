import subprocess
import os

class QemuManager:
    def __init__(self, vm_dir="/var/lib/qemu_vms"):
        self.vm_dir = vm_dir
        os.makedirs(vm_dir, exist_ok=True)

    def create_vm(self, name, image, mem, cpus, disk_size):
        vm_path = os.path.join(self.vm_dir, name)
        os.makedirs(vm_path, exist_ok=True)

        disk_path = os.path.join(vm_path, "disk.qcow2")
        subprocess.run(["qemu-img", "create", "-f", "qcow2", disk_path, f"{disk_size}G"], check=True)

        return {
            "name": name,
            "disk_path": disk_path,
            "mem": mem,
            "cpus": cpus,
            "status": "created"
        }

    def start_vm(self, name):
        vm_path = os.path.join(self.vm_dir, name)
        disk_path = os.path.join(vm_path, "disk.qcow2")

        command = [
            "qemu-system-x86_64",
            "-m", "512M",
            "-smp", "2",
            "-hda", disk_path,
            "-net", "nic",
            "-net", "user,hostfwd=tcp::2222-:22",
            "-display", "none"
        ]

        process = subprocess.Popen(command)
        return f"VM {name} started with PID {process.pid}"

    def stop_vm(self, name):
        try:
            subprocess.run(["pkill", "-f", f"qemu-system.*{name}"], check=True)
            return f"VM {name} stopped"
        except subprocess.CalledProcessError:
            return f"Error stopping VM {name}"

    def remove_vm(self, name):
        self.stop_vm(name)
        vm_path = os.path.join(self.vm_dir, name)
        subprocess.run(["rm", "-rf", vm_path])
        return f"VM {name} removed"
