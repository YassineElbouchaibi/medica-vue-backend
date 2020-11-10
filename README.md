# medica-vue-backend
MedicaVue's backend

# Usage (WIP)
1. Install docker on your machine. (TODO: Link to instructions)
2. Download app's static content (`storage` folder).
```sh
ggID='1QA3KtlUjZuCGfO_DQ-rUKRWfO1noNxWg'  
ggURL='https://drive.google.com/uc?export=download'  
filename="$(curl -sc /tmp/gcokie "${ggURL}&id=${ggID}" | grep -o '="uc-name.*</span>' | sed 's/.*">//;s/<.a> .*//')"  
getcode="$(awk '/_warning_/ {print $NF}' /tmp/gcokie)"  
curl -Lb /tmp/gcokie "${ggURL}&confirm=${getcode}&id=${ggID}" -o "${filename}"
unzip storage.zip
```
3. Pull container.
```sh
docker pull ghcr.io/yassineelbouchaibi/medica-vue.backend:latest
```
3. Start container (Replace <TEXT> with your values).
```sh
docker run -d -p <PORT_ON_YOUR_LOCAL_MACHINE>:80 \
  -v "</absolute/path/to/storage>":/storage \
  -e STORAGE_ROOT=/storage \
  medica-vue.backend
```
