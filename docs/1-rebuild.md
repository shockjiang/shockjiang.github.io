## rebuild personal homepage
- old/* is the source files of my personal homepage. Note all files are displayed online, but only 3 files are published: 1) my publications (src: old/_pages/publications.md) at https://shockjiang.github.io/publications/; 2) cv (src: old/_pages/cv.md) at https://shockjiang.github.io/. 3)Note that my peronsal informatin (src: old/_config.yml) shown at the left side pannel of the website.
- I want toe rebuild my personl homepage without changing its content (publication,cv, personal info), but with beautifuly UI.



## UI
- UI is top-down layout, top part should show my personal information. top part should contain three hide/show pannels, which are "News", "Publications" and "CV". the three pannels's link are aligned in one line, and allows visitors to click to show the pannel they want(the other pannels are hidden). News is displayed by default.

- allow to English and Chinese for personl information and CV. keep publication in English only.
- tag those papers, and show list all tags in top pannel. Tags should include "VLA", "Robot", "Pick&Place", "3D VL", "Open-Set Detection", "Keypoint Detection", "3D Detection", "3DGS", "Hand Reconstruction", "Object Reconstruction", "GPS-IMU-Wheel Fusion", and so on. Each paper can be associated with one or multple tags. you can derive more tags from the content of papers.
- color and font style should look like this web:http://14.103.44.161:18910/

## constraints
- do not change old/* files. create new files under ./
- files should be in .md (markdown) format, and friendly for me to add new items to "news", "publications", and "cv", so keep them seperately.

