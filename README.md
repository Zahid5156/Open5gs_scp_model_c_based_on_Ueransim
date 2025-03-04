## Project Title: Open5GS SCP Model C-UPF/SMF-UEs based on UERANSIM


Group Members:

Md Zahid Hasan - 1396470

Mahidul Islam Rana - 1502217

MD Fazley Rabbe - 1502895

Samsil Arefin - 1393091

## Introduction
This project demonstrates the installation of a 5G Standalone (SA) Core network with Open5GS, an open-source 5G core solution that prioritises performance, scalability, and resilience. Evolution in 5G technology has revolutionized wireless communications through ultra-high-speed data rates, reduced latency, and improved network capacity. An Open5GS-based 5G Standalone (SA) system allows for a scalable and modular implementation of 5G networks to enable high-level applications such as network slicing, ultra-reliable low-latency communication (URLLC), and large IoT connections. This work entails the deployment and testing of a 5G SA architecture with an Open5GS implementation, emphasizing core network functionality, data forwarding, and service chaining. Open5GS is an open-source 5G core network with support for important network functions such as the User Plane Function (UPF), Session Management Function (SMF), and Access and Mobility Management Function (AMF). In a 5G SA deployment, the User Equipment (UE) is connected to the network by the gNodeB (gNB), which manages radio access and communication with the 5G Core (5GC). The control plane, where session and mobility are managed, is separated from the user plane, which carries data. This separation enhances the efficiency, scalability, and flexibility of the network. One of the most important advantages of an Open5GS-based 5G SA system is the ability to deploy application-specific network slices. This project explains how various network services such as file sharing, SIP-based VoIP communication, and multimedia streaming can be integrated within specific network slices. File sharing uses protocols such as SMB, NFS, and FTP, allowing users to access remote data in a transparent manner. SIP facilitates real-time communication of video and audio, and it is managed by a SIP call server to forward, route, and confer calls. Multimedia is sent in an effective manner by streaming services based on protocols such as HLS, RTMP, and DASH. To implement these services, open-source software solutions such as Nextcloud, Owncast, and Kamailio are incorporated into the 5G network infrastructure. Nextcloud provides secure file storage and sharing, Owncast is an open-source streaming server that can be self-hosted, and Kamailio is a high-capacity SIP call server that supports thousands of concurrent calls. These solutions enhance the flexibility, security, and scalability of the 5G ecosystem. With the use of Open5GS in 5G SA deployment, this project will demonstrate the performance and viability of an open-source 5G core network. Network slicing and service integration point to the ability of 5G to support a range of applications, which will stimulate competition and innovation in the telecommunication industry. The findings of this project contribute to the understanding of 5G network architecture, service deployment, and the role of open-source technology in future communication networks.The project integrates automated scaling mechanisms that generate or enhance AMF, SMF, and UPF instances following the successful registration of every 10 UEs. This automated orchestration improves the network's overall efficiency.

## System Architecture

![image](https://github.com/user-attachments/assets/7386c5e4-9478-43ac-9e8b-f68c3ffd0b2a)

By describing the different components placed throughout the Control Plane and User Plane, the architecture that is being given offers a thorough examination of the design of a 5G network. The architecture is built to accommodate cutting-edge features like network slicing, effective data transfer, and the provision of a variety of services and file sharing. Network resource management and operation control are handled by a number of vital functions that make up the Control Plane. 
<details>
<summary>These include the following functions:</summary>
	
### UE Power On & Registration

- UE registers with AMF via gNB (N2).
- AMF, SMF, AUSF, UDM coordinate to authenticate the UE and allocate resources.

### PDU Session Setup	
- SMF sets up the user-plane tunnel with the UPF for the UE.
- UE obtains an IP address (or addresses) from the 5G core.

### Data Transfer
- UE sends traffic to the gNB, which goes to the UPF on N3.
- The UPF forwards traffic to the data network, applying policies from PCF/SMF.

### Network Slice or Policy
- If your deployment includes slicing, the NSSF might route the UE to a particular AMF/SMF instance or slice based on S-NSSAI.
- PCF enforces QoS, bandwidth, or charging policies.
 
### Orchestration & Scaling (Unique to our project)
- After every 10 UEs attach, the orchestrator can spin up a new AMF, SMF, or UPF container.
- The NRF updates the registry so newly spawned NFs become discoverable.
- Future UEs might register with the newly added network functions.

 </details>
 
 ## Definition and Abbreviations

| Short form | Full form |
| --- | --- |   
|Docker |                        Docker-desktop for containerize images |             
|SCP |                           Service Communication Proxy |
|AMF |                           Access and Mobility Management Function |
|NRF |                           Network Repository Function |
|UE |                            User Equipment |
|NSSF |                          Network Slice Selection Function |
|PDU |                           Protocol Data Unit |
|NGAP |                          Next Generation Application Protocol |
|SMF |                           Session Management Function |
|SD |                            Slice Differentiator |
|SST |                           Slice/Service Type |
|SDN |                           Software Defined Network |
|UPF |                           User Plane Function |
|RAN |                           Radio Access Network |
|PCF |                           Policy Control Function |
|SST |                           Service Set Type |
|SD |                            Service Domains |
|SIP |                           Session Initiation Protocol |
|UDM |	                        Unified Data Management |
|AUSF |	                        Authentication Server Function |
|UDR |	                        Unified Data Repository |


## Configuration

### Set Network IP

- Set the correct IP addresses in your .env file (where you have to update the real IP which is used for  your laptop Wi-Fi  address). The .env file is used to build the images using Build or Docker Compose, as well as deploying in Docker Compose. 

- You  can update the Docker with the buildx bake command but for our project, you don’t need to edit anything in the docker-bake.hcl file.

### Environment Variables

`OPEN5GS_VERSION` is the version of Open5GS to use.
- Accepted values are the tags, branches or commit IDs used in the Open5GS project
- Tested values: v2.7.2

`UBUNTU_VERSION` is the version of the ubuntu Docker image used as base for the containers.
- Accepted values are the tags used by Ubuntu in Docker Hub
- Tested values: jammy

`MONGODB_VERSION` is the version of the mongo Docker image used as database for Open5GS.
- Accepted values are the tags used by MongoDB in Docker Hub
- Tested values: 6.0

`NODE_VERSION` is the version of Node.js being used to build the Open5GS WebUI.
- Accepted values are the tags used by Node in Docker Hub for its bookworm-slim image and the Node.js dependency of Open5GS WebUI
- Tested values: 20

`192.168.2.35` is the IP address of the host running Docker. This modifies the `advertise` field in the `upf.yaml` config file for this to work when exposing the Docker containers network.

-	(if you want to run UERANSIM containers that directly create TUN interfaces on your host, you may need special permissions or host networking in place).

The `basic` deployment is prepared to work with external gNBs, exposing:
- `N2` control plane interface on the AMF using `SCTP port 38412`
- `N3` user plane  interface on the UPF using `UDP port 2152`
  
In most cases, no changes in docker-bake.hcl are required for an initial run unless you want a different Open5GS version or a custom build approach.


### Below table shows the configurations:

`Table 1`

| UE # | IMSI | DNN | OP/OPc |
| --- | --- | --- | --- |
| UE1 | 001011234567891 | Internet | OPC |
| UE2 | 001011234567892 | Internet | OPC |
| UE3 | 001011234567893 | Internet | OPC |
| UE4 | 001011234567894 | Internet | OPC |
| UE5 | 001011234567895 | Internet | OPC |
| UE6 | 001011234567896 | Internet | OPC |
| UE7 | 001011234567897 | Internet | OPC |
| UE8 | 001011234567898 | Internet | OPC |
| UE9 | 001011234567899 | Internet | OPC |
| UE10 | 001011234567810 | Internet | OPC |

`Table 2`

| SW & Role | IP address | OS | Memory (Min) | HDD(Min) |
| --- | --- | --- | --- | --- |
| Open5GS 5GC C-Plan | 10.33.33.8 - 10.33.33.9 | Ubuntu 22.04 | 4GB | 30GB |
| Open5GS 5GC U-Plan1 | 10.33.33.5 | Ubuntu 22.04 | 2GB | 20GB |
| UERANSIM RAN (gNodeB) | 10.33.33.15 - 10.33.33.16 | Ubuntu 22.04 | 2GB | 30GB |
| UERANSIM UE | 10.33.33.17 - 10.33.33.25 | Ubuntu 22.04 | 2GB | 20GB |

`Table 3`
| Network Function # | IP address | IP address on SBI | Supported S-NSSAI |
| --- | --- | --- | --- |
| AMF | 10.33.33.12 | 0.0.0.0 | SST: 1, SD: 1 |
| NSSF-SST1-SD1 | 10.33.33.9  | MSSf.Open5gs.org  | Sst : 1, sd: 1 |


### Build the project
<details>
<summary>Build it with Bake</summary>

>To construct our project, the advised method is to generate all the images first using a single command. Navigate to the project folder 'scpmodel-c-team-mobcomp', then open the terminal and execute the command shown below. Executing the command will generate all the images within Docker.

```bash
docker buildx bake
```

So now you see the images in docker so  the next step is to up the container for the images. To up the container of the images in docker we will follow the next step.

</details>

<details>

<summary>Build it with Docker Compose</summary>

Some deployments have the build instructions for the images (like the basic deployment), only depending of the base-open5gs image. Some other deployments download the images needed from container registries like Docker Hub or GitHub Container Registry (like the network-slicing deployment).

We will deploy the  ‘docker-compose.yaml’ files. Which is located in our project ‘compose-files’ folder. To deploy the ‘ docker-compose.yaml’ files we have to use this given command. After running the command now we can see our containers are running successfully in the Docker.

```bash
docker compose -f compose-files/scp/model-c/docker-compose.yaml --env-file .env up -d
```
</details>

<details>
<summary>Throughput Genaraton</summary>

## iPerf3:

iPerf3 is a network performance measurement tool used to generate and measure throughput between two endpoints. It helps test the speed and quality of a network connection by simulating TCP, UDP, and SCTP traffic.


</details>

<details>
<summary>To shut down the deployment</summary>

Now our project is successfully running so if you want you can check various connections from GNBs to Amf, and SMF then if you realize that now time to close the project you can just down the container. For that, you need the given command: 

```bash
docker compose -f compose-files/scp/model-c/docker-compose.yaml --env-file .env down
```
</details>

## Repository Structure
- `scpmodel-c-team-mobcomp` – This is our main project folder. Inside this folder, we have project files.
- `Documents` – In this folder has been used for uploading documents such as the pptx pdf file.
- `Testing_Results` – In this folder we storage our Webui Configuration photos.
- `Webui-Photos` – In this folder we storage our Webui Configuration photos.
- `compose-files/scp/model-c` - In this folder, we have docker-compose.yaml file.
- `configs/scp/model-c` - Config files for Open5GS (AMF, SMF, UPF, etc.)
- `images` – Docker files for building each network function (NF).
- `env` – Key environment variables for building and running the containers (e.g., IP addresses, base image versions, etc.).
- `LICENSE` 
- `Makefile` 
- `docker-bake.hcl` – Configuration for building images using docker buildx bake.

## Webui

This document provides an overview of how we manage 5G subscribers using the Open5GS WebUI (default port 9999). We demonstrate creating multiple users, each with its own unique IMSI and profile settings. <br>

<details>
<summary> Overview</summary>

<li>WebUI Default Port: 9999 </li>
<li>Subscribers: Each subscriber is identified by an IMSI and associated with specific keys (K, OP/OPc), AMF, and other parameters. </li>
<li>Profiles: We create profiles (e.g., User1, User2, etc.) to define bandwidth limits (e.g., 1 Gbps / 1 Gbps) or other QoS settings. </li>
<br>
</details>
	
<details>
<summary>Subscriber List</summary>

<br>
	


<br>
<li>Lists all active IMSIs (e.g., 001011234567810, 001011234567893, etc.).</li>
<li>Allows searching and filtering through the subscriber database.</li>
<br>

![Subscriber List](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Webui%20photos%20/1.jpeg)

</details>

<details>
<summary>Create Subscriber</summary>

	
<br>
<li>Shows how to add a new subscriber by specifying Profile, IMSI, Subscriber Key (K), Operator Key (OP/OPc), and AMF.</li>
<li>Other fields like UE-AMBR Downlink/Uplink can be configured here.</li>
<li>Enter the IMSI (unique for each user).</li>
<li>IMSI Format: Make sure each IMSI is unique to avoid conflicts. In a test environment, you can prepend 00101... or another consistent MCC/MNC scheme.</li>
<li>Restarting Services: After adding new subscribers, sometimes it’s useful to restart relevant Open5GS services (e.g., open5gs-amf, open5gs-smf) to ensure the changes are fully applied.
</li>

<br>

![Create Subscriber](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Webui%20photos%20/2.jpeg)

</details>

<details>
<summary>Profiles</summary>

<br>



<br>
<li>Displays user profiles (User1, User2, User3, etc.) each with a specified maximum uplink/downlink (e.g., 1 Gbps / 1 Gbps).</li>
<li>Profile Definition: You can assign different bandwidth or QoS parameters by creating multiple profiles (e.g., User1 to User10).</li>

<br>

![Create Subscriber](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Webui%20photos%20/3.jpeg)

</details>


## Testing 

<details>
<summary>Check Container Status: </summary>
Ensure that all NFs (AMF, SMF, UPF, NRF, SCP, AUSF, UDM, UDR, PCF, BSF) plus any orchestrator or RAN/UE containers are up and running.

```bash
Docker ps
```	
![Dockerps](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/docker%20ps.png)
In the top we attach out project screenshot which indicates that all the images/containers are running. 

</details>

<details>
<summary>gNb 1 and gNb 2  SCTP connection establishment and data passes:</summary>

### For gNb 1:
 
First you have to go the gNb1 logs for that you have to use below command

```bash
docker exec -it gnb1 sh
```

or

```bash
docker exec -it gnb1 bash
```

Secondly, the below given command is used for sctp_dann listening. When we will use this command then you will see sctp_dann is listening that means the gNb is waiting for packets/data. 

```bash
sctp_darn -H 0.0.0.0 -P 6000 -l 
```

Thirdly, you have to open another terminal and go to the gNb logs by using the given above command then you have to use the below given command. 

```bash
sctp_darn -H 0.0.0.0 -P 5000 -h 127.0.0.1 -p 6000 -s
```

![gNb 1](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/hello%20from%20gnb1.png)

### For gNb 2:
You have to follow the same process like gNb1 for checking sctp connection and passing data/packets.

```bash
docker exec -it gnb2 sh
```

![gNb 1](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/hello%20from%20gnb2.png)

</details>

<details>
<summary> SCTP connection and packets transfer with amf: </summary>
First, we can test SCTP connection for both the gNbs. To do this, we have to go gnb bash first by using the below command.

```bash
docker exec -it gnb1 bash
docker exec -it gnb2 bash
```
After that, we will see the assign IP addresses for both the gnb by using below command.

```bash
ip addr show
```

Now we will see the connection is ok or not by using the below command. 

```bash
sctp_test -H 10.33.33.16 -P 5001 -h amf.open5gs.org -p 38412 -s -d 2
``` 

## gNb1 transfer data with amf: 

![gNb amf 1](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/gnb1%20trasfer%20packets%20with%20amf.png)

## gNb2 transfer data with amf: 

![gNb amf 2](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/gnb2%20trasfer%20packets%20with%20amf.png)

By following the above pictures, we can see the connections are successfully established.

</details>


<details>
<summary>Running iPerf3 in a 5G Network Setup: </summary>

 ### Ensure both gNB and UE1 have iPerf3 installed.

- First you have to go to the bash for gNb1,gNb2 and UE1 to UE10. For that, you have to follow the command

```bash
docker exec -it gnb1 bash
docker exec -it gnb2 bash
docker exec -it ue1 bash
```

- iPerf3 needs to be installed on both devices (gNB and UE1) to send and receive network traffic.
- To install iPerf3 on most Linux-based systems, run the following command:
```bash
apt-get update && apt-get install -y iperf3
```
The command does the following: "apt-get update" refreshes the package list to get the latest versions.
"apt-get install -y iperf3" installs iPerf3 without requiring user confirmation.

### Start the iPerf3 Server on UE1

Configure UE1 to act as an iPerf3 server, ready to receive test traffic from gNB.
The iPerf3 server listens for incoming test traffic from the client. On UE10 (IP: 10.33.33.18).

```bash
iperf3 -s
```
iperf3 -s: Starts iPerf3 in server mode, allowing it to receive traffic from an iPerf3 client.
UE1 will now listen for incoming connections on port 5201 (default iPerf3 port).
The terminal will display a message confirming that iPerf3 is running as a server.

### Run the iPerf3 Client on gNB
Start the iPerf3 client on gNB to generate traffic towards the UE1 server.
The client actively sends test data to measure network performance. On gNB (IP: 10.33.33.15).

```bash
iperf3 -c 10.33.33.18
```
iperf3 -c <server-IP>: Starts iPerf3 in client mode, connecting to the server (UE1) at 10.33.33.18.
The client will send test packets to measure network throughput, jitter, and packet loss. 

## gnb1 to ue10 packets transfer successful: 

![gNb1 to UE 10](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/From%20gnb1%20to%20ue10%20packets%20transfer%20successful.png)

Now, we can follow the same process for gNb1 and gNb2 to all user interfaces. 

</details>

<details>
<summary>UDP Testing with iPerf3: </summary>
	
UDP (User Datagram Protocol) is often used in real-time applications like VoIP, video streaming, and gaming due to its low latency and connectionless nature. Unlike TCP, UDP does not provide retransmission or error correction, making it ideal for testing network jitter, packet loss, and real-time data transmission. By Command:

```bash
iperf3 -c 10.33.33.25 -u -b 100M
```
iperf3 -c 10.33.33.25 → Runs iPerf3 in client mode, connecting to the server at 10.33.33.25 (UE1 IP).
-u → Enables UDP mode (instead of the default TCP).
-b 100M → Sets the target bandwidth to 100 Mbps.

## UDP Performance test 100 mbps: 

![UDP](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/UDP%20Performance%20test%20100%20mbps.png)

</details>

<details>
<summary>Reverse Testing with iPerf3: </summary>

Reverse mode in iPerf3 allows testing uplink performance, where the UE (User Equipment) acts as the server, and the gNB (gNodeB) receives the data. This is useful for measuring uplink throughput, which is critical for applications like video uploads, live streaming, and cloud backups.

 ### Start the iPerf3 Server on UE1.
 This starts iPerf3 in server mode, waiting for a connection from the client. By command:
 
```bash
iperf3 -s
```
The command does the following: "apt-get update" refreshes the package list to get the latest versions.
"apt-get install -y iperf3" installs iPerf3 without requiring user confirmation.

### Run the iPerf3 Client in Reverse Mode on gNB

```bash
iperf3 -c 10.33.33.25 -R
```
## Gnb1 to ue1 Reverse packets testing: 

![Reverse](https://github.com/MobileComputingWiSe24-25/mobcom-teammblcp/blob/main/scpmodel-c-team-mobcomp/Testing_Results/Gnb1%20to%20ue1%20Reverse%20packets%20testing.png)

</details>


<details>
<summary>Simulate UEs: </summary>
UERANSIM containers will register with the AMF, get assigned IP addresses from the UPF, and connect to the DN.
By default, each UE has a single PDU session (IPv4).

</details>

<details>
<summary> Scaling / Upgrades </summary>
The orchestration logic may spin up additional AMF, UPF, SMF containers after every 10 UEs register.
Confirm new UEs are attached to the newly created NFs (if configured).

</details>

### Conclusion

This project showcases a thorough simulation of a 5G Core network with Open5GS and UERANSIM, successfully fulfilling the essential project criteria. The project effectively creates a working 5G standalone (SA) network environment by containerizing essential network functions (AMF, SMF, UPF, and others) using Docker and coordinating them with Docker Compose. UERANSIM facilitates authentic modeling of the RAN and several UEs, each initiating PDU sessions with appropriate IP allocations and data connectivity.

This project establishes a robust foundation for examining 5G core network architectures and delivers practical insights into containerization, network orchestration, and real-time traffic management, rendering it a valuable asset for further development and testing in mobile computing environments.

