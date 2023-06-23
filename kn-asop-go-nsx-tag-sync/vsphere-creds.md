kubectl create secret generic vsphere-credentials \
--type=kubernetes.io/basic-auth \
--from-literal=username='kn-ro@cpod-nsxv8.az-stc.cloud-garage.net' \
--from-literal=password='' \
--namespace vmware-functions
