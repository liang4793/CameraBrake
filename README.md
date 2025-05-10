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
2. **CameraBrake** can quickly turn off the camera via the service layer.  
3. **CameraBrake** can prevent the camera from turning on in order to protect privacy and security.  
4. **CameraBrake** is easy to use and light.  

## How to use  
Run `CameraBrake.py` or run `CameraBrake.exe` in the latest release.  

<img src="https://s2.loli.net/2025/05/06/veXL6dUfZyxW2BG.png" style="width: 260px; height: auto"/>
<img src="https://s2.loli.net/2025/05/06/29ZBXIdO3DU4z5r.png" style="width: 260px; height: auto"/>

<img src="https://s2.loli.net/2025/02/06/9O3HTlVhwcJIy2b.png" style="width: 260px; height: auto"/>
<img src="https://s2.loli.net/2025/02/06/SFhI6osjXmzTdnZ.png" style="width: 260px; height: auto"/>

<img src="https://s2.loli.net/2025/02/06/4T5gXuZnSFJqiAl.png" style="width: 260px; height: auto"/>

**main:**  
`Camera: On/Off` Show current status of camera.  
`Brake Camera! (Button)` Click to turn off the camera once. (Some programs can turn on the camera again)  
`Always Brake Camera (Switch)` Switch on to turn off the camera. (Doesn't allow the camera to be turned on again)  
`View Code / Leave Issues / Star (Button)` Jump to this Github page.  

**setting:**  
`Enable logger (Switch)` Switch on to log.  
`Open Log (Button)` Open log file.  
`Enable notifications (Switch)` Switch on to notify when camera is on.  
`Launch on Startup (Switch)` Switch on to launch on startup.  

**other:**  
`Minimize to Tray` Yes to minimize, No to exit.  
`Notifications` Camera status change notifications.  

## Poster
<img src="https://s2.loli.net/2025/02/06/cGH4qPC2rg5YVXB.png" style="width: auto; height: auto"/>

<a href="https://liang4793.github.io/" target="_blank"><img src="https://s2.loli.net/2024/07/12/4FNfqDjn231UgIG.png" style="width: 160px; height: auto"></a>
<a href="https://liang4793.github.io/" target="_blank"><img src="https://s2.loli.net/2024/07/12/EGrRQfFSNcvqxdh.png" style="width: 160px; height: auto"></a>
