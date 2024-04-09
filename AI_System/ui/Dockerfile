FROM node:20.12.1-alpine3.18

# Set the working directory in the container
WORKDIR /app

# Copy only requrirements to keep cache.
COPY ./package.json /app

# Install any needed packages specified in requirements.txt
RUN npm install

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD ["npm", "run", "dev"]
