import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.privatedns import PrivateDnsManagementClient
from azure.mgmt.privatedns.models import ARecord, RecordSet

# Configuration
SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", "your-subscription-id")
RESOURCE_GROUP = "your-resource-group"
DNS_ZONE_NAME = "your.private.dns.zone"
LOG_FILE = "aci_dns_sync.log"

# Mapping: ACI name -> DNS record name
aci_to_dns_map = {
    "aci-app1": "app1",
    "aci-app2": "app2",
    "aci-db": "db",
    "aci-api": "api",
    "aci-cache": "cache",
    "aci-worker": "worker",
    "aci-frontend": "frontend",
    "aci-backend": "backend",
    "aci-logging": "logging",
    "aci-monitoring": "monitoring",
    "aci-search": "search",
    "aci-analytics": "analytics",
    "aci-messaging": "messaging",
    "aci-queue": "queue",
    "aci-storage": "storage",
    "aci-loadbalancer": "loadbalancer",
    "aci-gateway": "gateway"
}

# Authenticate
credential = DefaultAzureCredential()
aci_client = ContainerInstanceManagementClient(credential, SUBSCRIPTION_ID)
dns_client = PrivateDnsManagementClient(credential, SUBSCRIPTION_ID)

with open(LOG_FILE, "a") as log:
    for aci_name, dns_name in aci_to_dns_map.items():
        try:
            container_group = aci_client.container_groups.get(RESOURCE_GROUP, aci_name)
            private_ip = container_group.ip_address.ip if container_group.ip_address else None

            if not private_ip:
                log.write(f"{aci_name} has no private IP. Skipping.\n")
                continue

            log.write(f"Updating {dns_name} -> {private_ip}\n")
            print(f"Updating {dns_name} -> {private_ip}")

            dns_client.record_sets.create_or_update(
                RESOURCE_GROUP,
                DNS_ZONE_NAME,
                dns_name,
                "A",
                RecordSet(
                    ttl=300,
                    a_records=[ARecord(ipv4_address=private_ip)]
                )
            )

        except Exception as e:
            log.write(f"Failed to update {dns_name}: {str(e)}\n")
            print(f"Failed to update {dns_name}: {str(e)}")
