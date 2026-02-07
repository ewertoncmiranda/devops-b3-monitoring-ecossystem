FROM eclipse-temurin:24-jdk-alpine
VOLUME /tmp
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENV SPRING_PROFILES_ACTIVE=docker
ENTRYPOINT ["java", \
            "-Dspring.profiles.active=dev", \
            "-jar", "/app.jar"]
