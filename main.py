from datetime import datetime, timedelta
import re
import os
from kubernetes import client, config, watch
 
config.load_kube_config()
v1 = client.CoreV1Api()
ns_regex_pattern = os.getenv("NAMESPACE_REGEX_PATTERN", "^review.*")
hours = int(os.getenv("KEEP_HOURS", "1"))
max_namespaces_to_delete = os.getenv("MAX_NAMESPACES_TO_DELETE", None)
if max_namespaces_to_delete is not None:
    max_namespaces_to_delete = int(max_namespaces_to_delete)
  
systemnamespac=["kube-system", "kube-public", "kube-node-lease", "default"] 
def delete_namespace_resources(namespace):
        v1.delete_collection_namespaced_pod(namespace)
        v1.delete_collection_namespaced_secret(namespace)
        v1.delete_namespace(namespace)

stream = watch.Watch().stream(v1.list_namespace)
deleted_namespaces = 0
while True:
    namespaces = v1.list_namespace().items
    namespaces_to_delete = []
    for namespace in namespaces:
        namespace_name = namespace.metadata.name
        if namespace_name not in systemnamespac and re.match(ns_regex_pattern, namespace_name) and datetime.utcnow() - namespace.metadata.creation_timestamp.replace(tzinfo=None) > timedelta(hours=hours):
            if namespace.status.phase != 'Terminating':
                namespaces_to_delete.append(namespace_name)
    namespaces_to_delete.sort(key=lambda x: v1.read_namespace(x).metadata.creation_timestamp)
    while namespaces_to_delete and (max_namespaces_to_delete is None or deleted_namespaces < max_namespaces_to_delete):
        namespace_name = namespaces_to_delete.pop(0)
        try:
            delete_namespace_resources(namespace_name)
            deleted_namespaces += 1
        except Exception as e:
            print(f"Error deleting namespace {namespace_name}: {str(e)}")
