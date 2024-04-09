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

### About 
-----
This is a template README for projects by Cogito NTNU.   

Here's the introduction about goal and summary of the project.
### Getting started
------

#### Prerequisites
In this section you put what is needed for the program to run.
For example: OS version, programs, libraries, etc.  

We'll be running Docker.
- You require Docker to be installed on your machine if you're building the images yourself.

#### Installation
In this Section you describe how to install this project in its intended environment.(i.e. how to get it to run)  

cd into your chosen project folder. Make sure there's a compose.yaml file there.
Run this in your terminal (Granted you have [Docker]([url](https://www.docker.com/get-started/)) on your system)
```
Docker compose up
```
If you make any code changes, remember to run
```
Docker compose build
```
before 'compose up' as the 'up' command doesn't rebuild the images.

#### Usage
------
In this section you describe how to use the program to obtain the desired result.  

### Architecture
We're using 4 backend services.
Mongodb server - Running on port 27017 - providing storage for chatlogs
Timeseries analysis - Running a python flask server, using tensorflow
LLM service - Running a python flask server, using langchain
Main endpoint : Nodejs - Providing static file hosting for the user interface, as well as rerouting to other services via API calls. 

#### Why do you route everything via Node, instead of calling the flask servers directly?
This way we can host everything on one machine, WITHOUT worrying about CORS.
1: CORS issues arise when a website tries to access information from a different domain than the one it's hosted on. This is a server issue, and can be fixed by allowing CORS, but is complexity we don't need right now.
2: By only having one endpoint, we can host this on a machine, with only one domain-name. Multiple direct endpoints would require multiple domain names to access, as they would be different servers. This requires setting up a load-balancer, which is not interest of the project.

### Team
------
<!--INSERT PICTURE OF TEAM-->
<div align="center">
<img src="https://cogito-ntnu.no/static/img/projects/erpokerpfpwekwpkerwer.png"></img>
</div>

Right to left: [@example](https://github.com/Jonrodtang)    [@example](https://github.com/Jonrodtang)    [@example](https://github.com/Jonrodtang)    [@example](https://github.com/Jonrodtang)  
#### Leader(s):
- [Jon Rødtang](https://github.com/Jonrodtang)
- [Example exampleson](https://github.com/Jonrodtang)

#### Team members:
- [Example exampleson](https://github.com/Jonrodtang)
-  [Examplette examplesen](https://github.com/Jonrodtang)
- [Examplar examples](https://github.com/Jonrodtang)

### License
------
Distributed under the MIT License. See `LICENSE` for more information.



### Credits
------
Template by [@JonRodtang](https://github.com/Jonrodtang) for  [@CogitoNTNU](https://github.com/CogitoNTNU)  <p align="right">(<a href="#top">back to top</a>)</p>
