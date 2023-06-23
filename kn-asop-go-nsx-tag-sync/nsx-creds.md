kubectl create secret generic nsx-credentials \
--type=kubernetes.io/basic-auth \
--from-literal=username='admin' \
--from-literal=password='' \
--namespace vmware-functions
