# Web-DataVisualization
Single Page Application for data visualization of files using HTML, CSS, Python and a little of JavaScript.

## Libraries
The principal libraries used were Flask for the app and bokeh for the plots. I tried to not use more libraries and develop the most part of the functionalities to practice the manage/format of the files and HTTP communications required to interact between the uploaded data and the plots, for this reason I also choose to use bokeh instead of the visualization libraries available in JS.

## How and why was built?
The most important point of the app is till the moment (08-2020) the app use his own folder to save the file (it's not a good practice but it facilitates the development of the app, permiting to not use externals), for this reason it was decided to always edit the file's name into a constant one, this implies that the app only can use one file in each case therefore the app was designed to only use in a local server.

The app only receives 4 types of formats ***.csv, .html, .json and .xsls***, then the file is formated to pass the data into the plot functions and to render the template. The app is contained in ***main.py*** its composed essentially of three parts, the render, the data collector and the plots; the render part update all the variables and sent it to the templates, the data collector part its a set of functions that handle the differents forms and finally the plots functions manage each one of the available plots that it was defined.

The auxiliar functions handle some minor procedures like the class to transform the data into lists or the particular functions for each plots of boke, in the templates there are a few lines of JS that receives the information to render the plots.


