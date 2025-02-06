# <img src="https://s2.loli.net/2023/05/26/IlQH3gnayib7Yvz.png" style="height: 24px;"> CameraBrake
**Camera privacy protection ver2.0!**  
A light and fast program that can quickly report and block camera service from opening.  
If you like it, please give me a star --->  

## Notes
**⚠️Only for Windows, tested on laptops & desktops running win10/11**  
If there are any questions, please leave issue or contact me.  
🔗Browse articles on: [Liang4793's Repository](https://liang4793.github.io/docs/P002-doc.html)  

## Realization
In a nutshell, a (Windows) service called `FrameServer` controls whether the camera is turned on or off.  
**CameraBrake** use `win32serviceutil` to check whether the camera is on and turn off the camera by stopping `FrameServer` service.  

## Introduction
1. **CameraBrake** can detect whether the camera service is occupied and report.  
2. **CameraBrake** can quickly turn off the camera.  
3. **CameraBrake** can prevent the camera from turning on in order to protect privacy and security.  
4. **CameraBrake** is easy to use and light.  

## How to use  
Run `CameraBrake.py` or run `CameraBrake.exe` in the latest release.   

<img src="https://s2.loli.net/2025/02/06/GplS4vemK3ZHUVr.png" style="width: 260px; height: auto"/>
<img src="https://s2.loli.net/2025/02/06/evVwhXn1f2JWxRK.png" style="width: 260px; height: auto"/>

<img src="https://s2.loli.net/2025/02/06/9O3HTlVhwcJIy2b.png" style="width: 260px; height: auto"/>
<img src="https://s2.loli.net/2025/02/06/SFhI6osjXmzTdnZ.png" style="width: 260px; height: auto"/>

<img src="https://s2.loli.net/2025/02/06/4T5gXuZnSFJqiAl.png" style="width: 260px; height: auto"/>

**main:**  
`Camera: On/Off` Show current status of camera.  
`brake camera! (Button)` Click to turn off the camera once. (Some programs can turn on the camera again)  
`always brake camera (Switch)` Switch on to turn off the camera. (Doesn't allow the camera to be turned on again)  

**setting:**  
`Logger (Switch)` Switch on to log.  
`Toaster (Switch)` Switch on to notify when camera is on.  

**other:**  
`Minimize to Tray` Yes to minimize, No to exit.  
`Report` Log & Windows notification.  

## Poster
<img src="https://s2.loli.net/2025/02/06/cGH4qPC2rg5YVXB.png" style="width: auto; height: auto"/>

<a href="https://liang4793.github.io/" target="_blank"><img src="https://s2.loli.net/2024/07/12/4FNfqDjn231UgIG.png" style="width: 160px; height: auto"></a>
<a href="https://liang4793.github.io/" target="_blank"><img src="https://s2.loli.net/2024/07/12/EGrRQfFSNcvqxdh.png" style="width: 160px; height: auto"></a>
