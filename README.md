# 🔄 Azure ACI Private DNS Sync

This script automates the process of synchronizing private IPs of Azure Container Instances (ACI) with A-records in an Azure Private DNS Zone.

## 🌐 Use Case

Many enterprise deployments rely on private networking and DNS resolution within a VNET. This tool helps ensure that ACI private IPs are always mapped correctly to hostnames in the private DNS zone.

Azure Container Instances (ACI) are a great way to run Docker images in a managed environment with minimal configuration effort — without needing to deploy a container runtime like Docker or manage a full Kubernetes cluster. However, despite their ease of use, ACIs present a few networking challenges when used inside a private virtual network:

An ACI instance connected to a private VNET does not propagate a DNS name (FQDN) automatically.

ACI does not support static private IPs. When a container is restarted or redeployed, it may be assigned a different private IP.

ACI does not support automatic DNS registration in Private DNS Zones like Azure Virtual Machines do.

Consequently, the A record in the private DNS zone will not update automatically, resulting in stale or incorrect DNS entries — which can break service discovery.

To overcome these limitations, this script (aci-dns-sync.py) ensures that DNS A-records are created or updated to reflect the current private IPs of ACI container groups. It can be used as:

A standalone automation script

A sidecar or startup container

A bootstrap step in deployment pipelines

This ensures that name resolution remains accurate across your private network environment.

## 📦 Features

- Fetches private IPs of ACI container groups in a given resource group
- Updates corresponding A-records in the Azure Private DNS Zone
- Supports logging for change tracking
- Gracefully handles cases where IP is unavailable or DNS update fails

## 🔧 Prerequisites

- Azure CLI authenticated with correct permissions
- ACI containers deployed in a resource group
- Private DNS Zone created
- Python 3.7+
- Required Azure SDK packages:

```bash
pip install azure-identity azure-mgmt-containerinstance azure-mgmt-privatedns
```

## ⚙️ Configuration

Set the following environment variable:

```bash
export AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
```

## 🚀 Running the Script

```bash
python3 aci_dns_sync.py
```

Log output will be stored in `aci_dns_sync.log`.

## 📝 Sample Output

```
Updating aci-analytics -> 10.60.1.10
Updating aci-frontend -> 10.60.1.4
Updating aci-backend -> 10.60.1.9
Updating aci-frontend -> 10.60.1.13
Updating aci-queue -> 10.60.1.5
Updating aci-cache -> 10.60.1.22

```

## 📂 Folder Structure

```
aci-dns-sync/
├── aci_dns_sync.py         # Main script
├── aci_dns_sync.log        # Runtime log (auto-generated)
├── LICENSE                 # MIT License
├── README.md               # Project documentation
└── .gitignore              # Ignore logs, Python cache
```

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙋‍♂️ Author

**Sukhanth** – DevOps Engineer passionate about automation in cloud-native environments.  
💼 [LinkedIn](https://www.linkedin.com/in/sukhanthn) | 📬 [Email](mailto:sukhanth.nandam@gmail.com)

## 🤝 Contributions

Pull requests are welcome! Open an issue first to discuss what you’d like to change.