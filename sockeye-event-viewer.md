kubectl -n vmware-functions create -f - <<EOF
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: sockeye
spec:
  template:
    metadata:
    spec:
      containers:
      - image: registry.cloud-garage.net/rguske/sockeye:v0.7.0
EOF


kn service update --scale 1 sockeye -n vmware-functions

kn trigger create sockeye --broker rabbitmq-broker --sink ksvc:sockeye -n vmware-functions