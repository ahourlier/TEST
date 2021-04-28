cat .deploy_keys/dev_firebase_key.json > app/firebase-key.json
cat .deploy_keys/dev_sa_key.json > app/sa-key.json

gcloud --quiet config set project app-oslo-dev
cp .env .env.dbak
gcloud secrets versions access latest --secret="backend_api_env" > .env

gcloud app deploy app.yaml manager.yaml dispatch.yaml queue.yaml --quiet

rm .env
mv .env.dbak .env

