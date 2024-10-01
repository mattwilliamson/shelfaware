# Dockerfile for React App
FROM node:16

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend app
COPY . .

# Build the React app
RUN npm run build

# Expose the port the React app will run on
EXPOSE 3000

# Serve the built React app using a lightweight web server (e.g., serve)
RUN npm install -g serve

# Command to serve the built app
CMD ["serve", "-s", "build"]
