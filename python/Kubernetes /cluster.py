from os import path
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from os import path
from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes.client import ApiClient


def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = kubernetes.client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance1 = kubernetes.client.CoreV1Api(api_client)
        return api_instance1
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_nodes(client_output):
    temp_dict={}
    temp_list=[]
    json_data=ApiClient().sanitize_for_serialization(client_output)
    if len(json_data["items"]) != 0:
        for node in json_data["items"]:
            temp_dict={
                "node": node["metadata"]["name"],
                "labels": node["metadata"]["labels"],
                }
            temp_list.append(temp_dict)
    return temp_list


def get_nodes(cluster_details, namespace="default",all_namespaces=False):
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
       
        node_list = client_api.list_node()
        data=__format_data_for_nodes(node_list)
        print (data)

def main():
    cluster_details={
        "bearer_roken":"",
        "api_server_endpoint":""
    }

    get_nodes(cluster_details)


if __name__ == "__main__":
    main()