# Dockerfile for the CoffeeKing frontend service.

# Use an Nginx base image to serve static files.
FROM nginx:alpine

# Copy the compiled frontend assets into the web root.  Since our
# frontend consists solely of static HTML, CSS and JS files there is
# no build step required.
COPY . /usr/share/nginx/html

# Expose the default HTTP port.
EXPOSE 80

# Nginx runs by default under the default command; no CMD override
# necessary.