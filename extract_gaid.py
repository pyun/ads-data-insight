import pandas as pd
import trino
from trino.auth import BasicAuthentication

# 读取CSV文件
csv_path = '/data/genai/ads-data-insight/data/input.csv'
df = pd.read_csv(csv_path, sep='|')

# 检查数据行数
row_count = len(df)
print(f"CSV文件共有 {row_count} 行数据")

# 提取gaid列
gaid_list = df['gaid'].tolist()

# 如果数据量小于1000条，直接输出列表
if row_count < 1000:
    print(gaid_list)
else:
    # 连接到Trino
    conn = trino.dbapi.connect(
        host='172.31.38.156',
        port=8889,
        user='hadoop',
        catalog='hive',
        schema='default',
    )

    cursor = conn.cursor()

    # 检查temp_gaid表是否存在，如果存在则删除
    cursor.execute("DROP TABLE IF EXISTS hive.default.temp_gaid")
    
    # 创建新的temp_gaid表
    cursor.execute("""
    CREATE TABLE hive.default.temp_gaid (
        gaid VARCHAR
    )
    """)
    
    # 插入数据
    batch_size = 1000  # 分批处理，避免单次插入过多数据
    total_inserted = 0

    for i in range(0, len(gaid_list), batch_size):
        batch = gaid_list[i:i+batch_size]
        values = ", ".join(f"('{g}')" for g in batch)
        insert_query = f"INSERT INTO hive.default.temp_gaid VALUES {values}"
        cursor.execute(insert_query)
        total_inserted += len(batch)
        print(f"已插入 {total_inserted}/{len(gaid_list)} 条数据")
    
    # 验证数据
    cursor.execute("SELECT COUNT(*) FROM hive.default.temp_gaid")
    count = cursor.fetchone()[0]
    print(f"temp_gaid表中共有 {count} 条数据")

    # 关闭连接
    cursor.close()
    conn.close()

    print("hive.default.temp_gaid")