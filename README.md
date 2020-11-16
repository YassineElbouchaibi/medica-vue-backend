<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- 
Here's a blank template to get started:
**To avoid retyping too much info. Do a search and replace with your text editor for the following:**
`github_username`, `repo_name`, `twitter_handle`, `email`
-->


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/YassineElbouchaibi/medica-vue-frontend">
    <img src="https://i.imgur.com/Py1JVG5.png" alt="Logo" height="80">
  </a>

  <h3 align="center">MedicaVue's backend</h3>

  <p align="center">
    Based on
    <a href="https://github.com/DebeshJha/2020-CBMS-DoubleU-Net">
      DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation
    </a>
    <br />
    <br />
    <a href="https://medica-vue.netlify.app">Website</a>
    ·
    <a href="https://github.com/YassineElbouchaibi/medica-vue-backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/YassineElbouchaibi/medica-vue-backend/issues">Request Feature</a>
    ·
    <a href="https://github.com/YassineElbouchaibi/medica-vue-frontend"><strong>Frontend</strong></a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

This was done in the context of a school project.

[![MedicaVue](https://i.imgur.com/thTIiEU.png)](https://medica-vue.netlify.app)

Backend Link: [https://github.com/YassineElbouchaibi/medica-vue-backend](https://github.com/YassineElbouchaibi/medica-vue-backend)

Frontend Link: [https://github.com/YassineElbouchaibi/medica-vue-frontend](https://github.com/YassineElbouchaibi/medica-vue-frontend)


### Built With

* [Python](https://www.python.org)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Tensorflow](https://www.tensorflow.org)
* [DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation](https://github.com/DebeshJha/2020-CBMS-DoubleU-Net)
* And many other great packages! Visit the [website](https://medica-vue.netlify.app) to get a list of all of them.


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Docker : 
    See instructions [here](https://docs.docker.com/engine/install/).

### Installation

1. Download app's static content (`storage` folder).
```sh
ggID='1QA3KtlUjZuCGfO_DQ-rUKRWfO1noNxWg'  
ggURL='https://drive.google.com/uc?export=download'  
filename="$(curl -sc /tmp/gcokie "${ggURL}&id=${ggID}" | grep -o '="uc-name.*</span>' | sed 's/.*">//;s/<.a> .*//')"  
getcode="$(awk '/_warning_/ {print $NF}' /tmp/gcokie)"  
curl -Lb /tmp/gcokie "${ggURL}&confirm=${getcode}&id=${ggID}" -o "${filename}"
unzip storage.zip
```

2. Pull container.
```sh
docker pull ghcr.io/yassineelbouchaibi/medica-vue.backend:latest
```

3. Start container (Replace <TEXT> with your values).
```sh
docker run -d -p <PORT_ON_YOUR_LOCAL_MACHINE>:80 \
  --name medica-vue.backend \
  -v "</absolute/path/to/storage>":/storage \
  -e STORAGE_ROOT=/storage \
  medica-vue.backend
```

<!-- USAGE EXAMPLES -->
## Usage

```sh
docker start medica-vue.backend
```



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/YassineElbouchaibi/medica-vue-backend/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Yassine El Bouchaibi - Contact info coming soon...

Open an issue.

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [DoubleU-Net: A Deep Convolutional Neural Network for Medical Image Segmentation](https://github.com/DebeshJha/2020-CBMS-DoubleU-Net)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/YassineElbouchaibi/medica-vue-backend.svg?style=flat-square
[contributors-url]: https://github.com/YassineElbouchaibi/medica-vue-backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/YassineElbouchaibi/medica-vue-backend.svg?style=flat-square
[forks-url]: https://github.com/YassineElbouchaibi/medica-vue-backend/network/members
[stars-shield]: https://img.shields.io/github/stars/YassineElbouchaibi/medica-vue-backend.svg?style=flat-square
[stars-url]: https://github.com/YassineElbouchaibi/medica-vue-backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/YassineElbouchaibi/medica-vue-backend.svg?style=flat-square
[issues-url]: https://github.com/YassineElbouchaibi/medica-vue-backend/issues
[license-shield]: https://img.shields.io/github/license/YassineElbouchaibi/medica-vue-backend.svg?style=flat-square
[license-url]: https://github.com/YassineElbouchaibi/medica-vue-backend/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/YassineElbouchaibi
