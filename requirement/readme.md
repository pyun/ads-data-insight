### 输入输出
输入：
	1. gaid：以csv、txt、xlsx等文件形式上传
	2. 包名
	3. 事件名称
	4. 时间周期
输出：gaid以及其对应的SAN渠道（二级、三级），以csv形式上传。
	1. dt
	2. pkg_name
	3. type/event_name
	4. second_channel
	5. affiliate_id
	6. nation
	7. gaid

### 示例1，当事件名称为install时
● gaid：`gaid文件.xlsx`
● 包名：com.example.game
● 事件名称：Install
● 时间周期：20250801 ~ 20250822
执行sql
```sql
    SELECT   DISTINCT dt
            ,pkg_name  
            ,second_channel  
            ,affiliate_id  
            ,target_geo AS nation
            ,gaid
            ,'pb' AS type 
    FROM t_conversion1  
    WHERE dt >= '20250501'                 
      AND dt <= '20250525'            
      AND pkg_name IN ('com.example.game')
      and gaid in ('27d356cc-5a9d-839c-a6f6-d37edc7dedbd',
      'e3982cde-6801-d316-cea0-46cfb1fb2cd7',
      '400eab3c-a7a0-5fb3-c86d-f2b4161456f9',
      '730f5193-d3a6-3629-8f0f-8051cfb7c1eb',
      '9480782c-e1cd-6aa8-ba34-c2b12a6a05c1',
      'b2dd9090-36f2-0401-bfe0-1c24568d1292',
      'eab3ab20-5ef2-31b3-1c90-f3541c352d23',
      '63c6db95-8f7c-21fe-3f0f-37b4429a85aa',
      '06c3b9d0-d63d-3735-7e1b-c7f97ab1e7da',
      'ad34fa63-9035-508b-37c7-f6071fff3074',
      'a6680771-9fb6-5423-ed36-18a20952fd4b',
      '2965f9b4-fc9c-f69b-7b54-b3e499f79528',
      '3982236f-fb10-e0c1-13eb-78ba092a6b63',
      '6207c8d2-9bcd-d047-8501-8047d207ecd5',
      '5bb41ce5-cbb9-d3dc-39d6-0c1b0b70bcfc',
      'b2877ed9-823b-510a-bb76-f21ade247415'
      	)
     
UNION ALL  
    SELECT   DISTINCT dt
            ,pkg_name  
            ,second_channel  
            ,affiliate_id  
            ,target_geo AS nation  -- 目标地理位置   
            ,gaid
            ,'reject' AS type 
    FROM t_conversion1
    WHERE dt >= '20250501'                 
      AND dt <= '20250525'            
      AND pkg_name IN ('com.example.game')
      and gaid in ('27d356cc-5a9d-839c-a6f6-d37edc7dedbd',
      'e3982cde-6801-d316-cea0-46cfb1fb2cd7',
      '400eab3c-a7a0-5fb3-c86d-f2b4161456f9',
      '730f5193-d3a6-3629-8f0f-8051cfb7c1eb',
      '9480782c-e1cd-6aa8-ba34-c2b12a6a05c1',
      'b2dd9090-36f2-0401-bfe0-1c24568d1292',
      'eab3ab20-5ef2-31b3-1c90-f3541c352d23',
      '63c6db95-8f7c-21fe-3f0f-37b4429a85aa',
      '06c3b9d0-d63d-3735-7e1b-c7f97ab1e7da',
      'ad34fa63-9035-508b-37c7-f6071fff3074',
      'a6680771-9fb6-5423-ed36-18a20952fd4b',
      '2965f9b4-fc9c-f69b-7b54-b3e499f79528',
      '3982236f-fb10-e0c1-13eb-78ba092a6b63',
      '6207c8d2-9bcd-d047-8501-8047d207ecd5',
      '5bb41ce5-cbb9-d3dc-39d6-0c1b0b70bcfc',
      'b2877ed9-823b-510a-bb76-f21ade247415'
      	)
```
### 示例2，当事件名称不是install时
● gaid：`gaid文件.xlsx`
● 包名：com.example.game
● 事件名称：purchase
● 时间周期：20250801 ~ 20250813

```sql
SELECT DISTINCT  dt
        ,pkg_name  
        ,second_channel  
        ,affiliate_id  
        ,target_geo AS nation  -- 目标地理位置  
        ,event_name 
        ,gaid
FROM t_event
WHERE dt >= '20250801'                   
  AND dt <= '20250813'         
  AND pkg_name IN ('com.example.game')   
  AND event_name='purchase'
  AND gaid IN ('6935eaaa-59f8-e6fd-5db0-1022c19b5039'
,'1c4c8566-fb3a-c023-2857-b93768eb5c3e'
,'470fde06-b6eb-49c6-ff39-61ccc5d3c9de'
,'fef6078b-86c4-9ae3-f724-449ec9dde9aa'
,'2ef1b463-2fb1-0e83-6702-e299fd398ac3'
,'b66a4e88-8a40-240a-9536-684ab26044f6'
,'8eef3e82-9cf6-fd30-b540-dc6b93d16995'
,'320e33f9-f3f2-2fd4-6330-b9106b79cc86'
,'977944d8-97b2-497e-822d-42960718bac1'
,'a9fd8264-2a3b-564f-145c-809f5ee91132'
,'d1ed99cc-b4b6-8bfe-929e-a43c523f1eb3'
  )
```

### 示例3，当gaid文件过大时（比如几十万）

如果本次gaid list样本量过大（14w），无法直接带入到SQL中执行（代码行数太多），因此，提供周期内这个包的所有明细，由需求方自行在EXCEL中匹配