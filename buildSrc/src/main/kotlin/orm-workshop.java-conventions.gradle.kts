plugins {
    id("org.springframework.boot")
    id("io.spring.dependency-management")
    id("io.freefair.lombok")
    id("java")
}

group = "com.tngtech.msd.orm"
version = "0.0.1-SNAPSHOT"

java {
    sourceCompatibility = org.gradle.api.JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-jdbc")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("jakarta.validation:jakarta.validation-api:3.1.0")
    runtimeOnly("org.postgresql:postgresql")
    runtimeOnly("org.hibernate:hibernate-validator:8.0.2.Final")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.named<Test>("test") {
	useJUnitPlatform()
}

dependencyLocking {
    lockAllConfigurations()
}
