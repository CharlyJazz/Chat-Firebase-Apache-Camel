FROM openjdk:11-jre-slim

ENV CAMEL_VERSION 3.14.0
ENV KAFKA_VERSION 2.8.0

WORKDIR /app

RUN wget https://downloads.apache.org/camel/${CAMEL_VERSION}/apache-camel-${CAMEL_VERSION}.tar.gz && \
    tar -xzf apache-camel-${CAMEL_VERSION}.tar.gz && \
    rm apache-camel-${CAMEL_VERSION}.tar.gz && \
    mv apache-camel-${CAMEL_VERSION} camel

RUN wget https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_2.13-${KAFKA_VERSION}.tgz && \
    tar -xzf kafka_2.13-${KAFKA_VERSION}.tgz && \
    rm kafka_2.13-${KAFKA_VERSION}.tgz && \
    mv kafka_2.13-${KAFKA_VERSION} kafka

COPY apache-camel-service-bus.jar /app

EXPOSE 9092

CMD ["java", "-jar", "apache-camel-service-bus.jar"]