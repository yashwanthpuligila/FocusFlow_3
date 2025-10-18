insert into rule(type, target_type, pattern, enabled, created_at, updated_at)
values ('BLACKLIST', 'WEBSITE', 'youtube.com', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Users are stored in MongoDB, not H2
-- Use the test_mongodb.py script or MongoDB Compass to add users


