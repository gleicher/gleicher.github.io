---
title: "2013 Qual: Real-Time Rendering"
draft: false
---

2013 Graphics Qual - readings from the Real Time Rendering book.
<!--more-->

Topics in RTR that are only mentioned briefly in FCG, but stillrequired. These are places where the text is the best starting point (as opposed to the older Qual reading list where we recommended the original source papers for the concepts). Topics where additional papers are needed are discussed in subsequent sections:

- Transformations \[RTR4\] - A lot of basic animation concepts (skinning, morphing) are hidden here.
- Visual Appearance \[RTR5\] - RTR organizes a lot of material scattered aboutFCG in one place. (gamma, anti-aliasing, compositing, ...)
- Rendering \[RTR7, RTR8, RTR9\] - The three chapters of RTR that cover "lighting and shading" give enough of the basic concepts of rendering. They generally are sufficient (see the rendering section below for a few exceptions). The discussions of "real-time hacks" can be skipped. 
    
    - Chapter 7 - Gives more details on the physics than necessary, but the intuitions are useful for understanding the more essential material. The concepts of surface appearance (like "what is the BRDF") are essential, the specific surface models given are not. 
    - Chapter 8 - The details of geometric lighting are less important than the idea of image-based lighting (using environment maps), including spherical harmonics.
    - Chapter 9 gives a good overview of global lighting, including introducing the light-path calculus (which is extremely important). The specific "hack algorithms" for faking global illumination in real-time rendering are not important for the qual (9.1.X, 9.2.5, 9.3 and 9.4 can be skipped).
    
    
    
- Non-Photorealistic Shading \[RTR11\] - a good introduction to the basics that should be augmented with the important papers below
- Polygonal Techniques \[RTR12\] - a good coverage of the basics that sufficiently replaces various sections of the older qual list.
- Surfaces \[RTR13\] - provides the basics of parametric surfaces and subdivision.

</div>
<div class="wikilastmod">Page last modified on June 20, 2013, at 03:14 PM</div>
