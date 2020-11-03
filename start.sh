#!/bin/bash
app="medica-vue.backend"
docker build -t ${app} .
docker run -d -p 56733:80 \
  --name=${app} \
  -v "/Users/yassineelbouchaibi/Documents/Cours/Automne 2020/INF8801A/Projet/storage":/storage \
  -e STORAGE_ROOT=/storage \
  ${app}