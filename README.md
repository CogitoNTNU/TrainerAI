<div id="top"></div>


<!--INSERT PICTURE REPRESENTATIVE OF PROJECT-->
<div align="center">
<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.Khns8mi5ov-qN64yFABHmAHaE7%26pid%3DApi&f=1"></img>
</div>
<p align="center">
<a href="https://github.com/CogitoNTNU/README-template/blob/main/LICENSE" alt="LICENSE">
        <img src="https://img.shields.io/badge/license-MIT-green"></img></a>

<a href="" alt="platform">
        <img src="https://img.shields.io/badge/platform-linux%7Cwindows%7CmacOS-lightgrey"></img></a>
<a href="" alt="version">
        <img src="https://img.shields.io/badge/version-0.0.1-blue"></img></a>
</p>
<h3 align="center">Personal Trainer AI</h3>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
   <li><a href="#team">Team</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

-----
### About 

Trainer AI is an LLM assistant agent with the goal of helping you workout more efficiently, and spend less time preparing workout sets, and analyzing data.
You talk to it like a personal coach, and it records your efforts, and lays plans for you to reach your goals.

------
### Getting started


#### Prerequisites
- You require Docker to be installed on your machine.
- You require an API key for OpenAI & LangSmith
        - OpenAI requires you to pay. Get a key from Cogito CTO if you're a member.
        - Langsmith doesn't require payment.

#### Installation
Create a .env file inside the folder 'AI_System'
Add the api keys:
OPENAI_API_KEY = ""
LANGSMITH_API_KEY = ""

cd into the AI_system folder. Make sure there's a compose.yaml file there.
Run this in your terminal (Granted you have [Docker]([url](https://www.docker.com/get-started/)) on your system)
```
docker compose up --build
```

-----
#### Usage
The UI is accessible at https://localhost:3000

------
### Architecture
We're using 4 backend services.
Mongodb server - Running on port 27017 - providing storage for chatlogs
Timeseries analysis - Running a python flask server, using tensorflow
LLM service - Running a python flask server, using langchain
Main endpoint : Nodejs - Providing static file hosting for the user interface, as well as rerouting to other services via API calls. 

#### Why do you route everything via Node, instead of calling the flask servers directly?
1: CORS
2: Node is better suited for exposing directly to web.

------
### Team

<!--INSERT PICTURE OF TEAM-->
<div align="center">
<img src=""></img>
</div>

#### Leader(s):
- [William Schmidt](https://github.com/williammrs)

#### Team members:
- [Tryggve Klevstul-Jensen](https://github.com/tryggvek)
-  [Eldar Alvik](https://github.com/PolarUgle)
- [James](https://github.com/JamesP62)

------
### License
Distributed under the MIT License. See `LICENSE` for more information.

------
### Credits
Template by [@JonRodtang](https://github.com/Jonrodtang) for  [@CogitoNTNU](https://github.com/CogitoNTNU)  <p align="right">(<a href="#top">back to top</a>)</p>
