---
title: "2013 Qual: Readings from Foundations of Computer Graphics"
draft: false
---

Textbook readings - materials from an undergrad class.

<!--more-->

In the order they appear in \[FCG\] - note that \[FCG\] is not always the preferred resource for the topic.

- Mathematical Basics \[FCG 2,5\]: Linear Algebra (including the SVD), interpolation
- Raster Imaging \[FCG 3\]: The content of this chapter of FCG is really just a preliminary sketch of things that come later.
- Ray Tracing \[FCG 4,13\]: the basic ideas are important, the ray/primitive intersection methods are not. (see the realistic rendering section below)
- Transformations, Viewing \[FCG 6,7\]\[RTR 4\]: FCG misses some important things like Quaternions (covered in RTR). RTR also includes the basics of other important ideas like morphing and vertex blending (although, other readings may enhance those). Jehee Lee's survey of the issues in rotations (below) is required for concepts like Quaternions and rotation vectors.
- The "Traditional" Graphics Pipeline \[FCG 2,8\] \[RTR2\]: This includes basic rasterization algorithms, clipping, and anti-aliasing.
- Image and Signal Processing \[FCG 9\]: 
- Lighting (local shading models) \[FCG 10\] \[OGL\] \[RTR\]:The OpenGL bookdescribes the model well, but the syntactic details of using it withinOpenGL are an ugly legacy that is not required. Stylized shading is another seperate topic.
- Texturing \[FCG 11\]\[RTR 6\]: RTR is the key resource here, includingsampling issues and strategies, and tricks for using texturing to achieve other means.
- Data Structures / Acceleration Algorithms \[FCG 12\] \[RTR 14\]: \[FCG12\] is a hodgepodge of basic stuff that everyone should know. \[RTR 14\] has too much detail, but replaces the Visibility section of the old qual reading list
- Curves and Surfaces \[FCG 15\]\[RTR 13\]: \[FCG\] completely omits surfaces. The topic (especially subdivision and meshes) deserves more than what RTR provides (more readings below), but its a good start.
- Animation \[FCG16\]: Covers the basics (which might not appear in the more detailed papers below).
- Programmable Graphics Hardware \[FCG 18\]\[RTR 3\]\[OGL 15\]:While this is amoving target, the key ideas of the pipeline seem to have settled overthe past few years. Students should understand the idea behind ashading language (like GLSL) as a reflection of the computationalmodel, but the syntactic details of particular languages are unimportant.
- Interactive Architectures \[FCG19\]: The chapter has a lot of stuff that's way too basic, but students should understand event models vs. polling and MVC.
- Color \[FCG21\]: Students should understand both the perceptual foundations (presented, in an albeit obtuse way in FCG), as well as more practical issues
- Visual Perception \[FCG22\]: The FCG chapter is a good starting point.
- Tone Reproduction \[FCG23\]: Clearly a case where the basic issues and ideas are more important than the details. 
- Global Illumination \[FCG 24\] \[RTR 9\]: The basic concepts are important, but the methods are not well described in either text (and not important). See the Photorealistic Rendering section below. The hacks described in RTR for achieving global illumination effection within the standard rendering pipeline (like 40 pages of shadow mapping tricks) are not essential for the qual, except for the way they bring in the issues of what kinds of effects are difficult to achieve with various rendering approaches.
- Visualization \[FCG27,28\]: In the future, this will be an entire section of the qual. For now, what is here serves as a good introduction.

</div>
