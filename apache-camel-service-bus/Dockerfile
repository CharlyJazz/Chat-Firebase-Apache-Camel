# Use an official Maven image
FROM maven:3.8.4-openjdk-17

# Set the working directory in the container
WORKDIR /app

# Copy the source code and POM file to the container
COPY src/ /app/src/
COPY pom.xml /app/

# Build the application to create the .jar file (skip tests)
RUN mvn package -DskipTests

# Specify the command to run the Spring Boot application
CMD ["java", "-jar", "target/apache-camel-service-bus-1.0.0.jar"]