# Namespace Cleaner

This code is a python script that deletes Kubernetes namespaces based on a regex pattern and the age of the namespace. It also prevents system namespaces from being deleted.

## Requirements
- Python 3.6+
- Kubernetes Client

## Usage
The following environment variables can be used to configure the script:
- `NAMESPACE_REGEX_PATTERN` - The regex pattern to match against when selecting namespaces for deletion (defaults to `^review.*`)
- `KEEP_HOURS` - The number of hours a namespace must exist before it is eligible for deletion (defaults to `1`)
- `MAX_NAMESPACES_TO_DELETE` - The maximum number of namespaces to delete in one run (defaults to `None`)

## License
This project is licensed under the MIT License.