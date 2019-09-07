Live API actively expands. Documentation which laid out by Hanz Petrov ([API_MakeDoc](http://remotescripts.blogspot.ru/p/support-files.html)) becomes too cumbersome. It is difficult to search, to compare different versions, to understand what features are added, that has changed.

I spent the time and has made more advanced design of this unofficial documentation:

https://nsuspray.github.io/Live_API_Doc/

I have tried to simplify the search and navigation, to make design more accessible. It has a function of comparing different versions with independent displaying additions, changes, matches. I think you will understand.

New XML documentation files (*8.2.7.xml*, *9.0.6.xml* e.t.c.) are obtained from [the original files of Hans Petrov](https://julienbayle.studio/ableton-live-midi-remote-scripts/#liveAPI) using a *LiveApiXmlHierarchical.py*, *LiveAPI.xsl* is connected to them, which translates data to an HTML document, styled with CSS, the dynamics is implemented by JavaScript using jQuery (including side menu dynamics *jquery.singlePageNav-multilevel.js*). *CompareXmlTree.py* generates difference XML files (*8.2.7-9.0.6.xml* e.t.c.) from source XML (*8.2.7.xml* vs *9.0.6.xml* e.t.c.).