SELECT client_addr, application_name, count(*) 
FROM pg_stat_activity 
WHERE datname = 'sonarqube'
GROUP BY client_addr, application_name;


SHOW shared_buffers;
SHOW work_mem;
SHOW maintenance_work_mem;
SHOW effective_cache_size;
SHOW temp_buffers;

SELECT datname, temp_bytes
FROM pg_stat_database
ORDER BY temp_bytes DESC;

SELECT uuid, status, task_type, created_at
FROM ce_activity
WHERE status IN ('PENDING', 'IN_PROGRESS', 'FAILED', 'CANCELED')
ORDER BY created_at DESC;

DELETE FROM ce_queue;
DELETE FROM ce_activity WHERE status IN ('FAILED', 'CANCELED');

CREATE TABLE ce_queue_backup AS SELECT * FROM ce_queue;
CREATE TABLE ce_activity_backup AS SELECT * FROM ce_activity;


SELECT NOW();



SELECT status, COUNT(*) FROM ce_activity GROUP BY stat

###
CREATE TABLE ce_activity_backup AS SELECT * FROM ce_activity;

DELETE FROM ce_activity WHERE status = 'CANCELED';
SELECT status, COUNT(*) FROM ce_activity GROUP BY status;



