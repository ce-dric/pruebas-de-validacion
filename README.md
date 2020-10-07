<h1 align="center">pruebas-de-validacion</h1>
<p>
  <a href="https://github.com/Odin-son/pruebas-de-validacion/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> acceptance testing, image viewer for validation
>
> ![test](etc/test.gif)
## Author

👤 **Changwoo Song**

> Github: [@Odin-son](https://github.com/Odin-son) <br>
> LinkedIn: [@mdsd12](https://linkedin.com/in/mdsd12) <br>
> 
> This project was inspired from [acbetter](https://gist.github.com/acbetter/e7d0c600fdc0865f4b0ee05a17b858f2)
## Requirements
* library
    * PyQt5

## Getting Started
> in case of using virtualenv,
```bash
$ virtualenv [env_name] --python=python3.7
$ source [en_name]/bin/activate
```
> in case of using anaconda,
```bash
$ conda create -n [env_name] python=3.7
$ conda activate [env_name]
```
> install required library(CLI)
```
$ pip install PyQt5 
```

## How to use
> execute `viewer.py`
```
$ cd path/to/project
$ cd src/
$ python viewer.py
```
![test](etc/demo1.png)
>
> using `Open Both...`, there is required structure below:
```
# use the same filename for each sub-directory
ROOT
├── original
│   ├── image.png
│   └── ...
└── mask
    ├── image.png
    └── ...
```
> after all, following menu items (will be update)

## Troubleshooting
```
$ cd path/to/project
$ cd src/
$ python viewer.py 
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

Aborted (core dumped)
```
> sudo apt-get install "^libxcb.*" libx11-xcb-dev libglu1-mesa-dev libxrender-dev

## 📝 License
Copyright © 2020 [Changwoo Song](https://github.com/Odin-son).
This project is [MIT](https://github.com/Odin-son/pruebas-de-validacion/blob/main/LICENSE) licensed.
