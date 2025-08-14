INSERT INTO t_event (dt, pkg_name, event_name, second_channel, affiliate_id, nation, gaid)
SELECT 
    -- 生成过去30天内的随机日期
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY) AS dt,
    -- 随机选择包名
    ELT(FLOOR(RAND() * 5) + 1, 
        'com.example.game', 
        'com.example.social', 
        'com.example.shopping', 
        'com.example.news', 
        'com.example.weather') AS pkg_name,
    -- 随机选择事件名
    ELT(FLOOR(RAND() * 6) + 1, 
        'install', 
        'open', 
        'register', 
        'purchase', 
        'share', 
        'uninstall') AS event_name,
    -- 随机选择二级渠道
    ELT(FLOOR(RAND() * 4) + 1, 
        'organic', 
        'cpc', 
        'social', 
        'email') AS second_channel,
    -- 生成随机联盟ID
    CONCAT('aff_', FLOOR(RAND() * 1000)) AS affiliate_id,
    -- 随机选择国家
    ELT(FLOOR(RAND() * 10) + 1, 
        'US', 'CN', 'JP', 'DE', 'UK', 
        'FR', 'CA', 'AU', 'IN', 'BR') AS nation,
    -- 生成随机GAID (UUID格式)
    CONCAT(
        SUBSTRING(MD5(RAND()) FROM 1 FOR 8), '-',
        SUBSTRING(MD5(RAND()) FROM 1 FOR 4), '-',
        SUBSTRING(MD5(RAND()) FROM 1 FOR 4), '-',
        SUBSTRING(MD5(RAND()) FROM 1 FOR 4), '-',
        SUBSTRING(MD5(RAND()) FROM 1 FOR 12)
    ) AS gaid
FROM 
    -- 生成1000行数据 (通过交叉连接生成足够的行数)
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t2,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t3
LIMIT 1000;

INSERT INTO t_conversion1 (dt, pkg_name, second_channel, affiliate_id, nation, gaid)
SELECT 
    -- 生成过去30天内的随机日期
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY) AS dt,
    -- 随机选择包名
    ELT(FLOOR(RAND() * 5) + 1, 
        'com.example.game', 
        'com.example.social', 
        'com.example.shopping', 
        'com.example.news', 
        'com.example.weather') AS pkg_name,
    -- 随机选择二级渠道
    ELT(FLOOR(RAND() * 4) + 1, 
        'organic', 
        'cpc', 
        'social', 
        'email') AS second_channel,
    -- 生成随机联盟ID
    CONCAT('aff_', FLOOR(RAND() * 1000)) AS affiliate_id,
    -- 随机选择国家
    ELT(FLOOR(RAND() * 10) + 1, 
        'US', 'CN', 'JP', 'DE', 'UK', 
        'FR', 'CA', 'AU', 'IN', 'BR') AS nation,
    -- 生成随机GAID (UUID格式)
    CONCAT(
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 8), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 4), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 4), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 4), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 12)
    
    ) AS gaid
FROM 
    -- 生成1000行数据 (通过交叉连接生成足够的行数)
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t2,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t3
LIMIT 1000;

INSERT INTO t_conversion2 (dt, pkg_name, second_channel, affiliate_id, nation, gaid)
SELECT 
    -- 生成过去30天内的随机日期
    DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY) AS dt,
    -- 随机选择包名
    ELT(FLOOR(RAND() * 5) + 1, 
        'com.example.game', 
        'com.example.social', 
        'com.example.shopping', 
        'com.example.news', 
        'com.example.weather') AS pkg_name,
    -- 随机选择二级渠道
    ELT(FLOOR(RAND() * 4) + 1, 
        'organic', 
        'cpc', 
        'social', 
        'email') AS second_channel,
    -- 生成随机联盟ID
    CONCAT('aff_', FLOOR(RAND() * 1000)) AS affiliate_id,
    -- 随机选择国家
    ELT(FLOOR(RAND() * 10) + 1, 
        'US', 'CN', 'JP', 'DE', 'UK', 
        'FR', 'CA', 'AU', 'IN', 'BR') AS nation,
    -- 生成随机GAID (UUID格式)
    CONCAT(
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 8), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 4), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 4), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 4), '-',
        SUBSTRING(SHA2(CONCAT(RAND(), UUID()), 256) FROM 1 FOR 12)
    
    ) AS gaid
FROM 
    -- 生成1000行数据 (通过交叉连接生成足够的行数)
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t2,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) t3
LIMIT 1000;
