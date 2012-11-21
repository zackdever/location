Uber clients are able to store favorite locations for easy pickup
requests. Create a backend and a frontend for managing favorite locations.

This is a simple exercise, but organize, design and test your code as if it
were going into production.

When you're done, host it somewhere and provide us with a URL and a tarball
or Git repo with the code.

Backend

Using the language (Python preferred), libraries and data store of your
choosing, create a JSON in/out RESTful API for managing favorite locations.
Stay away from Django or Rails, but microframeworks like Flask (preferred),
Sinatra or Express are fine.

Attributes of a favorite location object include:


- id
- lat
- lng
- address (e.g. 800 Market Street, San Francisco, CA 94114)
- name (e.g. Work)


Frontend

Using JavaScript, Backbone.js and any other libraries of your choosing,
create an interface to access the API. User should be able to:


- Create a new location
- Read/view a location, and a collection of all locations
- Update an existing location
- Delete a location


The UX is up to you, with a couple of constraints:


- Incorporate a map
- Geocode the address so the user is not required to enter lat/lng


Extras

If you like, get creative and do whatever else you like on the backend
and/or frontend to show off.
