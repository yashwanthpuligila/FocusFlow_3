package com.focusflow.admin.dto;

import com.focusflow.admin.model.User;

public class AuthResponse {
    public boolean success;
    public String message;
    public UserInfo user;

    public static class UserInfo {
        public String id;
        public String username;
        public String email;
        public String fullName;
        
        public static UserInfo from(User user) {
            UserInfo info = new UserInfo();
            info.id = user.getId();
            info.username = user.getUsername();
            info.email = user.getEmail();
            info.fullName = user.getFullName();
            return info;
        }
    }
}