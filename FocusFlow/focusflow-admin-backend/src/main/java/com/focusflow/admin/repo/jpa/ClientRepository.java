package com.focusflow.admin.repo.jpa;

import com.focusflow.admin.model.Client;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClientRepository extends JpaRepository<Client, Long> { }
