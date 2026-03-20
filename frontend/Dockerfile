# Use Node.js for the 2026 frontend build
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the Vite port
EXPOSE 3000

# Start the Project Aeterna UI
CMD ["npm", "run", "dev", "--", "--host"]
