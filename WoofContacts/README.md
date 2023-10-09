# WoofContacts

#### Video Demo: https://youtu.be/5_UgRtXbylc

#### Description: The project is a basic contact storing web-app using python, flask and databases in SQL. Using the navbar, I was able to create a navigation bar through which the user can  be taken from one page to another. The first thing to do was the design in the pages. Most of the design was inspired by CS50 Finance as it was very appealing to me. Using different background colors and a new favicon of my dog (Kumo), I made it unique and aestheticized to my own style. It's somewhat dark themed as that is less straining on the eyes. 

#### The project basically acts as a place where a user can store their contacts, similar to a phone book. The contacts are shown in accordance to alphabetic order. The web-app allows the user to store their contacts in a consolidated environment. Search for one of those contacts, delete a contact or block a contact and view the blocked contacts. Before getting access to any of those features, however, the user must first register an account, and remain logged in.

#### The project itself used wraps which allowed me to decorate functions with log in required to allow users to only access a particular page if and only if they are logged in. The functions performed specific actions. The add contacts function added a particular contact to a database in which the user id is stored, hence only allowing that specific user to access those contacts. Similary the add contacts function took in the contact details and added those too to the contact database. The contact database also has a parameter called blocked which is boolean and hence allows easier access to non-blocked or blocked contacts.

#### The index function described a function which displayed all the non-blocked contacts of a user in the page in the form of a table. The headers were green to indicate that  these are good (non-blocked) contacts. This called a simple database execution with SELECT that allowed me to show only the non-blocked contacts of a particular user.

#### The blocked function was pretty similar to the index function, calling another SELECT function in SQL that in which I set a condition where the blocked boolean type was set to 1 (i.e. True). Here again, the user is redirected to another page where they can view their blocked contacts. The table headers were red to indicate that these contacts are the bad ones (i.e. the blocked ones).

#### The search function again queried the database that allowed the user to search for a given contact in their contact list. This redirected the user to a searched page where they were shown the contact details of the contact that they had searched for.

#### The delete function simply deleted a contact by removing them from the database for that user.

#### The block function changed the blocked parameter of the contacts database that set the blocked parameter to 1, effectively blocking them.

#### I also made several HTML files. The layout.html file was to set up the basic design of the webpage to prevent rewriting a LOT of code. The other files were used to set up the pages for the index, search, delete, block and blocked functions. In index and block, I used HTML Table tags to help me provide the contact details in a tabular form. The others took in an input as a parameter with a button to submit their input and then performed the respective functions.

#### Using the concepts taught in CS50x I was able to complete this project and it was really fun. Took a good amount of time!