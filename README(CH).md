# Emergency-Brakes
<p>
    <img src="https://img.shields.io/badge/Author-Liang4793-blue" alt="Author" />
    <img src="https://img.shields.io/github/license/liang4793/Emergency-Brakes" alt="license" />
    <img src="https://img.shields.io/badge/Language-Python-yellow" alt="Language" />
    <img src="https://img.shields.io/badge/Platform-windows-lightgrey" alt="Platform" />
</p>

### [English](/README.md) | 简体中文

**摄像头隐私保护！**  
快速地检测、报告并阻止摄像头服务的开启   
如果你喜欢的话，给我一个star吧 --->  

## 笔记
遇到任何问题请留下issue或与我联系  
🔗在 [Liang4793's Repository](https://liang4793.github.io/docs/project_docs/E-B_doc.html) 浏览该文章

## 介绍
1. **Emergency-Brakes** 可以检测摄像头服务是否被占用并报告  
2. **Emergency-Brakes** 可以快速关闭摄像头
3. **Emergency-Brakes** 可以防止摄像头打开，以保护隐私和安全。

## 如何使用

<figure class="half">
    <img src="https://s2.loli.net/2022/06/13/GHqgpKXF6lVUQT3.jpg" style="width: 260px; height: auto"/>
    <img src="https://s2.loli.net/2022/06/13/NKHTy4Ql7xjcviG.jpg" style="width: 260px; height: auto"/>
</figure>

**main:**  
`Camera: On/Off` 显示摄像头当前状态  
`brake camera! (Button)` 单击以关闭摄像头一次 (部分程序会再次开启摄像头)  
`always brake camera (Switch)` 打开以关闭摄像头 (阻止摄像头被再次开启)

**setting:**  
`Logger (Switch)` 打开以记录日志  
`Toaster (Switch)` 打开以开启摄像头通知

## 实现方式
一个叫做 `FrameServer` 的(Windows)服务控制摄像头的开启或关闭  
**Emergency-Brakes** 使用 `win32serviceutil` 来检查摄像头是否被开启并通过停止 `FrameServer` 服务来关闭摄像头
