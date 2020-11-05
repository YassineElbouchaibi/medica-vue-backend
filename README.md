# medica-vue-backend
MedicaVue's backend

# Usage (WIP)
1. Install docker on your machine. (TODO: Link to instructions)
2. Download app's static content (`storage` folder). (TODO: Add download link)
3. Pull container.
```sh
docker pull ghcr.io/yassineelbouchaibi/medica-vue.backend:latest
```
3. Start container (Replace <TEXT> with your values).
```sh
docker run -d -p <PORT_ON_YOUR_LOCAL_MACHINE>:80 \
  -v "<path/to/storage>":/storage \
  -e STORAGE_ROOT=/storage \
  medica-vue.backend
```
