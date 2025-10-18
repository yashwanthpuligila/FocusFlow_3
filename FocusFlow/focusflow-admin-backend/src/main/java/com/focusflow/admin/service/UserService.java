package com.focusflow.admin.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.focusflow.admin.dto.AuthResponse;
import com.focusflow.admin.dto.LoginRequest;
import com.focusflow.admin.dto.RegisterRequest;
import com.focusflow.admin.model.User;
import com.focusflow.admin.repo.mongo.UserRepository;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public AuthResponse login(LoginRequest request) {
        AuthResponse response = new AuthResponse();
        
        if (request.username == null || request.password == null) {
            response.success = false;
            response.message = "Username and password are required";
            return response;
        }

        Optional<User> userOpt = userRepository.findByUsername(request.username);
        
        if (userOpt.isEmpty()) {
            response.success = false;
            response.message = "Invalid username or password";
            return response;
        }

        User user = userOpt.get();
        
        // In production, use BCrypt or similar for password hashing
        if (!user.getPassword().equals(request.password)) {
            response.success = false;
            response.message = "Invalid username or password";
            return response;
        }

        if (!user.isActive()) {
            response.success = false;
            response.message = "Account is disabled";
            return response;
        }

        response.success = true;
        response.message = "Login successful";
        response.user = AuthResponse.UserInfo.from(user);
        return response;
    }

    public AuthResponse register(RegisterRequest request) {
        AuthResponse response = new AuthResponse();
        
        // Validation
        if (request.username == null || request.username.trim().isEmpty()) {
            response.success = false;
            response.message = "Username is required";
            return response;
        }
        
        if (request.password == null || request.password.length() < 4) {
            response.success = false;
            response.message = "Password must be at least 4 characters";
            return response;
        }
        
        if (request.email == null || !request.email.contains("@")) {
            response.success = false;
            response.message = "Valid email is required";
            return response;
        }

        // Check if username exists
        if (userRepository.existsByUsername(request.username)) {
            response.success = false;
            response.message = "Username already exists";
            return response;
        }

        // Check if email exists
        if (userRepository.existsByEmail(request.email)) {
            response.success = false;
            response.message = "Email already registered";
            return response;
        }

        // Create new user
        User user = new User();
        user.setUsername(request.username.trim());
        user.setPassword(request.password); // In production, hash this
        user.setEmail(request.email.trim());
        user.setFullName(request.fullName != null ? request.fullName.trim() : "");
        user.setActive(true);

        User savedUser = userRepository.save(user);

        response.success = true;
        response.message = "Registration successful";
        response.user = AuthResponse.UserInfo.from(savedUser);
        return response;
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
}