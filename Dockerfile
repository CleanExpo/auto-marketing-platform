# Use official Node.js 20 image
FROM node:20

# Set working directory
WORKDIR /usr/src/app

# Copy dependency files and install
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Build TypeScript if present
RUN npm run build || echo "No build step"

# Start app (change to 'npm run dev' for dev env)
CMD ["npm", "start"]
