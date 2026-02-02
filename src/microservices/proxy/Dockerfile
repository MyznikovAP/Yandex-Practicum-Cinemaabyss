# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install app dependencies
COPY package.json ./
RUN npm install --production

# Copy application code
COPY . ./

# Expose port (default 8000, can be overridden by env)
EXPOSE 8000

# Start the service
CMD ["npm", "start"]