# Flask-BDA
Flask-BDA is built using a Flask Rapid Application Development (RAD) called [Flask-BDA]().

# Know how to style a MD document properly
[https://www.markdownguide.org/basic-syntax/](https://www.markdownguide.org/basic-syntax/)

# Ajax Requests

> Ajax requests are made using [</> htmx](https://htmx.org/) by default
> htmx is a dependency-free library that allows you to access AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes, so you can build modern user interfaces with the simplicity and power of hypertext. For a details on how to use htmx, please refer to the [docs](https://htmx.org/docs/) and for a full reference on the functionality, please refer to: [https://htmx.org/reference/](https://htmx.org/reference/)

You can use htmx to implement many common UX patterns, such as Active Search:
```
<input type="text" name="q" 
    hx-get="/trigger_delay" 
    hx-trigger="keyup changed delay:500ms" 
    hx-target="#search-results" 
    placeholder="Search..."/>

<div id="search-results"></div>
```
This input named q will issue a request to `/trigger_delay` 500 milliseconds after a key up event if the input has been changed and inserts the results into the div with the id search-results.