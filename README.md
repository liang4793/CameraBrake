# CameraBrake
**Camera privacy protection**  
Quickly report and block camera service from opening.  
If you like it, please give me a star --->  

## Notes
**⚠️Only for Windows, tested on laptops running win10/11**  
If there are any questions, please leave issue or contact me.  
🔗Browse articles on: [Liang4793's Repository](https://liang4793.github.io/docs/project_docs/E-B_doc.html)

## Realization
A (Windows) service called `FrameServer` controls whether the camera is turned on or off.  
**CameraBrake** use `win32serviceutil` to check whether the camera is on and turn off the camera by stopping `FrameServer` service.

## Introduction
1. **CameraBrake** can detect whether the camera service is occupied and report.  
2. **CameraBrake** can quickly turn off the camera.
3. **CameraBrake** can prevent the camera from turning on in order to protect privacy and security.

## How to use

<figure class="half">
    <img src="https://s2.loli.net/2023/05/21/XDvcHAE1tnaZbUg.png" style="width: 260px; height: auto"/>
    <img src="https://s2.loli.net/2023/05/21/P2mSfjocRQAHnMd.png" style="width: 260px; height: auto"/>
</figure>

**main:**  
`Camera: On/Off` Show current status of camera.  
`brake camera! (Button)` Click to turn off the camera once. (Some programs can turn on the camera again)  
`always brake camera (Switch)` Switch on to 
turn off the camera. (Doesn't allow the camera to be turned on again)

**setting:**  
`Logger (Switch)` Switch on to log.  
`Toaster (Switch)` Switch on to notify when camera is on.