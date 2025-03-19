import os
import subprocess

class QemuManager:
    def __init__(self, vm_dir=r'C:\var\lib\qemu_vms'):
        self.vm_dir = vm_dir
        os.makedirs(vm_dir, exist_ok=True)

    def create_vm(self, name, iso_path, mem, cpus, disk_size):
        vm_path = os.path.join(self.vm_dir, name)
        os.makedirs(vm_path, exist_ok=True)

        disk_path = os.path.join(vm_path, f"{name}_disk.qcow2")
        
        # Создаем виртуальный диск
        subprocess.run([
            "qemu-img", "create", "-f", "qcow2", disk_path, f"{disk_size}G"
        ], check=True)

        return {
            "name": name,
            "disk_path": disk_path,
            "iso_path": iso_path,
            "mem": mem,
            "cpus": cpus,
            "status": "created"
        }

    def start_vm_install(self, name):
        """ Запускает VM с ISO для установки ОС """
        vm_path = os.path.join(self.vm_dir, name)
        disk_path = os.path.join(vm_path, "ubuntu.qcow2")
        iso_path = r"C:\var\lib\qemu_vms\ubuntu.iso"  # Убедитесь, что ISO в этом пути

        command = [
            "qemu-system-x86_64",
            "-m", "1024M",  # 1GB RAM
            "-smp", "2",  # 2 CPU
            "-boot", "d",  # Загружаемся с CD-ROM
            "-cdrom", iso_path,  # Указываем ISO
            "-drive", f"file={disk_path},format=qcow2",  # Указываем жесткий диск
            "-net", "nic",
            "-net", "user,hostfwd=tcp::2222-:22",
            "-display", "default"
        ]

        process = subprocess.Popen(command, shell=True)
        return f"VM {name} started for installation with PID {process.pid}"

    def start_vm(self, name):
        """ Запускает установленную систему без ISO """
        vm_path = os.path.join(self.vm_dir, name)
        disk_path = os.path.join(vm_path, "ubuntu.qcow2")

        command = [
            "qemu-system-x86_64",
            "-m", "1024M",
            "-smp", "2",
            "-boot", "c",  # Загружаемся с диска
            "-drive", f"file={disk_path},format=qcow2",
            "-net", "nic",
            "-net", "user,hostfwd=tcp::2222-:22",
            "-display", "default"
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
