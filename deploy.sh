set -ex

# [START getting_started_gce_create_instance]
MY_INSTANCE_NAME="gpu-app-instance"
ZONE="us-east1-b"

# Specify the GPU type and count
GPU_TYPE=nvidia-tesla-p100  # You can change this to the desired GPU type (e.g., nvidia-tesla-v100)
GPU_COUNT=1  # Number of GPUs

# Specify the desired boot disk size (in GB)
BOOT_DISK_SIZE=100  # You can change this to the desired size

gcloud compute instances create $MY_INSTANCE_NAME \
    --image-family=debian-10 \
    --image-project=debian-cloud \
    --machine-type=n1-standard-4 \
    --boot-disk-size=$BOOT_DISK_SIZE \
    --accelerator="type=$GPU_TYPE,count=$GPU_COUNT" \
    --maintenance-policy TERMINATE \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=startup-script.sh \
    --zone $ZONE \
    --tags http-server
# [END getting_started_gce_create_instance]

gcloud compute firewall-rules create default-allow-http-8080 \
    --allow tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 8080 access to http-server"
