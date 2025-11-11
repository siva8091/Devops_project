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

