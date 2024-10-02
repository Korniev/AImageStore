<a name="readme-top"></a>
<br />
<div align="center">
  <h3 align="center">AImageStore</h3>

  <p align="center">
    AImageStore is a Django-based web application for all people who love animals and want to know more about them.
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li>
      <a href="#show-funcionality">Show funcionality</a>
    </li>
    <li><a href="#contributors">Contributors</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot](https://github.com/Korniev/AImageStore/blob/main/img_readme/main.png)

AImageStore is a web app for animal lovers which has next implemented features:
* Registration
* Login
* User authentication through Google
* Google Drive
* Profile information
* Classify image with animal
* Reading wikipedia about animals
* Save images into Google Drive
* Chatbot
* Language switching

So the project leverages a pre-trained neural network model to efficiently classify
images, specifically identifying animals in uploaded images. It also integrates with Google Drive,
allowing users to save and organize their classified images directly in their Drive. The application
features user authentication through Google, language switching (supporting English, Ukrainian, and
Spanish) and a chatbot powered by the OpenAI API was implemented.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
* ![Docker](https://img.shields.io/badge/docker-blue?style=for-the-badge&logo=docker&logoColor=white)
* ![Docker Compose](https://img.shields.io/badge/docker_compose-blue?style=for-the-badge&logo=docker&logoColor=white)
* ![Jupyter Notebook](https://img.shields.io/badge/jupyter_notebook-orange?style=for-the-badge&logo=jupyter&logoColor=white)
* ![JavaScript](https://img.shields.io/badge/javascript-yellow?style=for-the-badge&logo=javascript&logoColor=white)
* ![HTML](https://img.shields.io/badge/html-orange?style=for-the-badge&logo=html5&logoColor=white)
* ![Tailwind CSS](https://img.shields.io/badge/tailwindcss-0F172A?style=for-the-badge&logo=tailwindcss)
* ![Google Drive](https://img.shields.io/badge/google_drive-white?style=for-thebadge&logo=google%20drive&logoColor=white&color=%23EA4336)
* ![Google Auth](https://img.shields.io/badge/GoogleConnect-brightgreen?style=for-the-badge&labelColor=black&logo=google)
* ![Open AI API](https://img.shields.io/badge/-OpenAI%20API-eee?style=for-the-badge&logo=openai&logoColor=412991)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get installed our web app you should follow these simple steps:

1. Clone the repository:

```bash
https://github.com/Korniev/AIma
```

2. Change to the project's directory:
```bash
cd AImageStore
```

3. You can make a docker compose for easy use of our application. You should write a following command in the terminal:

```bash
docker compose up --build
```

4. Now you can go to your browser and tap:

```bash
http://0.0.0.0:8000
```

5. To stop running docker compose you shoud write next command in terminal:

```bash
docker compose stop
```

6. To remove docker compose you should write next command in terminal:

```bash
docker compose down
```

Also you have posibility to start using AImageStore in dev mode!
You should check file doc.md where you can find guide how to run web app on dev mode via ngrok.

We hope you enjoy our web application! :)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Show funcionality -->
## Show funcionality
