import click
import subprocess
import yaml
import os
import docker

client = docker.from_env()

CONFIG_DIR = "/app/configs/scp/model-c"  # Path inside the ue-manager container
UE_CONFIG_TEMPLATE = """
supi: '{imsi}'
mcc: '001'
mnc: '01'

key: '{key}'
op: '00000000000000000000000000000000'
opType: 'OPC'
amf: '8000'
imei: '356938035643803'
imeiSv: '4370816125816151'

gnbSearchList:
  - gnb.ueransim.org

uacAic:
  mps: false
  mcs: false

uacAcc:
  normalClass: 0
  class11: false
  class12: false
  class13: false
  class14: false
  class15: false

sessions:
  - type: 'IPv4'
    apn: 'internet'
    slice:
      sst: 1
      sd: '{sd}'

configured-nssai:
  - sst: 1
    sd: '{sd}'

default-nssai:
  - sst: 1
    sd: '{sd}'

integrity:
  IA1: true
  IA2: true
  IA3: true

ciphering:
  EA1: true
  EA2: true
  EA3: true

integrityMaxRate:
  uplink: 'full'
  downlink: 'full'
"""

@click.group()
def cli():
    """CLI for managing UEs in the 5G test environment."""
    pass

@cli.command()
@click.option('--num', type=int, required=True, help='UE number to add')
@click.option('--imsi', required=True, help='IMSI of the UE')
@click.option('--key', required=True, help='Subscriber Key')
@click.option('--opc', required=True, help='Subscriber OPC')
@click.option('--sd', required=False, default='1', help='Slice Differentiator (SD)')
def add(num, imsi, key, opc, sd):
    """Adds a new UE.

    This involves:
        1. Generating a UERANSIM config file (ueN.yaml).
        2. Enabling the UE's profile and starting the container using docker-compose.
    """
    try:
        # 1. Generate UERANSIM config file
        config_filename = generate_ue_config(num, imsi, key, opc, sd)
        print(f"Generated UERANSIM config: {config_filename}")

        # 2. Enable and start the UE container
        subprocess.run(['docker-compose', '--profile', f'ue{num}', 'up', '-d'], check=True, cwd="/app")
        print(f"UE {num} added and container started.")

        # 3. (Optional) Trigger core network scaling if needed
        # scale_core_services_if_needed()

    except Exception as e:
        print(f"Error adding UE: {e}")

@cli.command()
@click.option('--num', type=int, required=True, help='UE number to remove')
def remove(num):
    """Removes a UE.

    This involves:
        1. Stopping and removing the UE container.
        2. Removing the corresponding ueN.yaml config file.
    """
    try:
        # 1. Stop and remove the UE container
        subprocess.run(['docker-compose', 'stop', f'ue{num}'], check=True, cwd="/app")
        subprocess.run(['docker-compose', 'rm', '-f', f'ue{num}'], check=True, cwd="/app")

        # 2. Remove the UERANSIM config file
        config_filename = os.path.join(CONFIG_DIR, f"ue{num}.yaml")
        if os.path.exists(config_filename):
            os.remove(config_filename)
            print(f"Removed UERANSIM config file: {config_filename}")
        else:
            print(f"Config file not found: {config_filename}")

        print(f"UE {num} removed.")

    except Exception as e:
        print(f"Error removing UE: {e}")

@cli.command()
@click.option('--all', is_flag=True, help='Show all UEs (including stopped)')
def list(all):
    """Lists available and active UEs."""
    try:
        running_ues = []
        stopped_ues = []

        # Get project name from environment variable or default
        project_name = os.environ.get('COMPOSE_PROJECT_NAME', 'your_project_name') # Default value if not set

        for container in client.containers.list(all=all, filters={"label": f"com.docker.compose.project={project_name}"}):
            container_name = container.name
            if container_name.startswith('ue') and container_name[2:].isdigit():
                ue_num = int(container_name[2:])
                config_filename = os.path.join(CONFIG_DIR, f"ue{ue_num}.yaml")

                if container.status == "running":
                    running_ues.append(ue_num)
                elif all:
                    stopped_ues.append(ue_num)

        print("Running UEs:")
        if running_ues:
            for ue_num in sorted(running_ues):
                print(f"  ue{ue_num} (running, config: {os.path.join(CONFIG_DIR, f'ue{ue_num}.yaml')})")
        else:
            print("  None")

        if all:
            print("\nStopped UEs:")
            if stopped_ues:
                for ue_num in sorted(stopped_ues):
                    print(f"  ue{ue_num} (stopped, config: {os.path.join(CONFIG_DIR, f'ue{ue_num}.yaml')})")
            else:
                print("  None")

    except Exception as e:
        print(f"Error listing UEs: {e}")

def generate_ue_config(ue_num, imsi, key, opc, sd=None):
    """Generates a UERANSIM configuration file (ueN.yaml) for a UE."""
    config_filename = os.path.join(CONFIG_DIR, f"ue{ue_num}.yaml")

    config_content = UE_CONFIG_TEMPLATE.format(imsi=imsi, key=key, opc=opc, sd=sd if sd is not None else '1')

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(config_filename), exist_ok=True)

    with open(config_filename, "w") as f:
        f.write(config_content)

    return config_filename

if __name__ == '__main__':
    cli()