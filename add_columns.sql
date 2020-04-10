ALTER TABLE sessions
    ADD ShowSuccessOrMiss CHAR(3) DEFAULT 'yes';
ALTER TABLE sessions
    ADD TimetoshowPlaySpeed TINYINT(1) DEFAULT 1;
ALTER TABLE sessions
    ADD TimetoshowReleaseSpeed TINYINT(1) DEFAULT 1;