package com.focusflow.admin.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
@EnableJpaRepositories(basePackages = "com.focusflow.admin.repo.jpa")
@EnableMongoRepositories(basePackages = "com.focusflow.admin.repo.mongo")
public class RepositoryConfig {
    // This configuration separates JPA and MongoDB repositories
    // JPA repositories: com.focusflow.admin.repo.jpa
    // MongoDB repositories: com.focusflow.admin.repo.mongo
}
