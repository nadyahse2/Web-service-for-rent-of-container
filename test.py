import os

vm_dir=r"C:\var\lib\qemu_vms"
vm_path = os.path.join(vm_dir, 'ubuntu.iso')
iso_path = r"C:\var\lib\qemu_vms\ubuntu.iso"
disk_path = os.path.join(vm_path, "ubuntu.qcow2")

if not os.path.exists(iso_path):
    print(f"Файл {iso_path} не найден!")
else:
    print("Файл найден.")