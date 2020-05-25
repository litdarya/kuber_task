SERVICE=$1

kubectl config set-context $(kubectl config current-context) 
helm upgrade -f ${SERVICE}/values.yaml --install ${SERVICE} ${SERVICE}
