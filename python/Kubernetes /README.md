### Creating Cluster and Node via Terraform

### Prerequisites

* an AWS account with the IAM permissions listed on the EKS module documentation,
* a configured AWS CLI
* AWS IAM Authenticator
* kubectl

1. ### Install AWSCLI

 To install AWSCLI run the following command:


### Configure AWS 

To configure awscli

```
aws configure
```
```
provider "aws"{
region = "us-east-1"
access_key = "Your_Access_Key"
secret_key = "Your_Secret_Key"
}
```

. ### Creating Cluster & nodes via terraform

To create cluster and node you have to create one directory and terraform files inside that directory as :

```
mkdir <dir_name>
```

Files named as:

```
* vpc.tf
* security-group.tf
* eks-cluster.tf
* outputs.tf
* versions.tf
```

In **vpc.tf** we'll add providers (aws_secret_key , aws_access_key)


Now run the Terraform command to Create the Cluster and nodes on EKS:


### Initialize Terraform workspace

```
terraform init
```

### To see Terraformlogs 

```
terraform plan
```

### Provisioning the EKS Cluster

```
terraform apply
```

4. ### Configure Kubectl

```
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)
```

5. ### Create Kubernetes Service Account For API Access 

**Create a devops-tools namespace.**

```
kubectl create namespace devops-tools

```

**Create a service account named “api-service-account” in devops-tools namespace**

```
kubectl create serviceaccount api-service-account -n devops-tools
```

**We can do this by creating a manifest file also.** 

[Access Your File(serviceaccount.yaml)](./Cluster%20Management/yamls/api-service-account.yaml)

```
kubectl apply -f api-service-account.yaml
```

5. ### Create a Cluster Role

**Created a clusterRole named api-cluster-role using this manifest file**

[Access Your File(api-cluster-role.yaml)](./Cluster%20Management/yamls/api-cluster-role.yaml)

```
kubectl apply -f api-cluster-role.yaml
```

**To get the list of available API resources**

```
kubectl api-resources
```

6. ### Create a CluserRole Binding

**We have the ClusterRole and service account, it needs to be mapped together using RoleBinding.**

[Access Your File(api-cluster-role.yaml)](./Cluster%20Management/yamls/RoleBinding.yaml)

```
kubectl apply -f api-rolebinding.yaml
```

7. ###  Validate Service Account Access Using kubectl

**To validate the clusterrole binding, we can use can-i commands to validate the API access assuming a service account in a specific namespace**

**This command can checks if the api-service-account in the devops-tools namespace can list the pods**

```
kubectl auth can-i get pods --as=system:serviceaccount:devops-tools:api-service-account
```

**To check if the service account has permissions to delete deployments**

```
kubectl auth can-i delete deployments --as=system:serviceaccount:devops-tools:api-service-account
```

8. ### Validate Service Account Access Using API call

**To use a service account with an HTTP call, you need to have the token associated with the service account**

1. Get the secret name associated with the api-service-account.Use the secret name to get the base64 decoded token. It will be used as a bearer token in the API call.

```
kubectl get secrets
```

```
kubectl get secrets  api-service-account-token-pgtrr  -o=jsonpath='{.data.token}' -n devops-tools | base64 -D
```
2. Get the cluster endpoint to validate the API access. The following command will display the cluster endpoint (IP, DNS).

```
kubectl get endpoints | grep kubernetes
```

9. ### Install python and kubernetes client



```
pip install kubernetes
```

10. ### Now we can start run different python script.

```
python3 ingress.py
```
