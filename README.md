# My-html-Stew
I made a very bad 0$ budget html thing like bs4 because my mobile python app didnt have it installed, it was a fun project, I hope you try to break it

HOW TO USE THIS THING (MESSY_STEW):

**you need the 'requests' module too, yuh**

1. you gotta make a parsed html object first like bs4 does! fortunately we don't gotta do any crazy stuff because I wanna feel lazy:

> #example code for making the object
> stew = MessyStew("https://youtube.com")

2. now that we have our 'stew' tree-object, we can finally fiddle with it and stuff! right now the current things we can do are:

2A. find - finds the first matching tag and its brick attribute(name, parent, data, attributes, babies(child))
example:
>  img_test = stew.find("img","attributes")
>  the first argument specifies which "tag" we want from the tree, and the second one is what attribute of the tag we want to get simple stuff

3. use the things you got! whether it be collecting data, scraping links, or any other stuff (idk any other things right now so I'll just say it to make it look like theres more) you can think of!

4. this one's for me, I wanna thank you for reading through this whole thing 👍
