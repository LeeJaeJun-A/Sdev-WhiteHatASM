# Use the official Node.js image as a parent image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy the entire frontend directory into the container at /app/frontend
COPY . /app/frontend

# Set the working directory to /app/frontend
WORKDIR /app/frontend

# Install dependencies
RUN npm install

# Build the SvelteKit application
RUN npm run build

# Expose port 3000 for the SvelteKit application
EXPOSE 3000

# Command to run the SvelteKit application
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
