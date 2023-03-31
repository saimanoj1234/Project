#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyspark.sql.functions import *
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Read from MySQL").config("spark.sql.warehouse.dir","/user/hive/warehouse").enableHiveSupport().getOrCreate()

jdbcHostname = "savvients-classroom.cefqqlyrxn3k.us-west-2.rds.amazonaws.com"
jdbcPort = 3306
jdbcDatabase = "practical_exercise"
jdbcUsername = "sav_proj"
jdbcPassword = "authenticate"
jdbcUrl = "jdbc:mysql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)

connectionProperties = {
    "user": jdbcUsername,
    "password": jdbcPassword,
    "driver": "com.mysql.jdbc.Driver"
}
spark.sql("SHOW DATABASES").show()
spark.sql("USE MANOJ")
df = spark.read.jdbc(url=jdbcUrl, table="user", properties=connectionProperties)
df.show()
df.write.mode("overwrite").saveAsTable("MANOJ.us")
#df.write.format('csv').save("/user/hadoop/manoj/user.csv")
df2 = spark.read.jdbc(url=jdbcUrl, table="activitylog", properties=connectionProperties)
df2.show()
df2.write.mode("overwrite").saveAsTable("MANOJ.ac")
#df2.write.format('csv').save("/user/hadoop/tswi2")
spark.sql("SELECT * FROM MANOJ.us").show(5)

spark.sql("CREATE  TABLE IF NOT EXISTS MANOJ.user_upload_dump_06 (user_id int,file_name string,time_stmp bigint) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','STORED AS TEXTFILE tblproperties('skip.header.line.count'='1')")
#spark.sql("LOAD DATA INPATH  '/user/hadoop/manoj/user_upload_dump_2023_03_06.csv' OVERWRITE INTO TABLE MANOJ.user_upload_dump_06")


## USER_TOTAL TABLE
spark.sql("CREATE TABLE IF NOT EXISTS  MANOJ.user_total (time_ran timestamp,total_users int,users_added int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','STORED AS TEXTFILE")

spark.sql("CREATE TABLE IF NOT EXISTS MANOJ.user_repport (user_id int,total_updates int,total_inserts int,total_deletes int,last_activity_type string,is_active boolean,upload_count int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE")
spark.sql("""
    INSERT INTO user_total
    SELECT
        t1.time_ran,
        t1.total_users,
        t1.total_users - COALESCE(t2.total_users, 0) AS users_added
    FROM (
        SELECT CURRENT_TIMESTAMP() AS time_ran, COUNT(*) AS total_users
        FROM us
    ) t1
    LEFT JOIN (
        SELECT time_ran, total_users
        FROM user_total
    ) t2 ON t1.time_ran > t2.time_ran
    ORDER BY t1.time_ran
""")
spark.sql("select * from user_total").show();

## USER REPORT TABLE


spark.sql("""
    INSERT OVERWRITE TABLE user_repport
    SELECT
        us.id AS user_id,
        COALESCE(SUM(CASE WHEN ac.type = 'UPDATE' THEN 1 ELSE 0 END)) AS total_updates,
        COALESCE(SUM(CASE WHEN ac.type = 'INSERT' THEN 1 ELSE 0 END)) AS total_inserts,
        COALESCE(SUM(CASE WHEN ac.type = 'DELETE' THEN 1 ELSE 0 END)) AS total_deletes,
        MAX(ac.type) AS last_activity_type,
        CASE WHEN CAST(from_unixtime(MAX(ac.timestamp)) AS DATE)  >= DATE_SUB(CURRENT_TIMESTAMP(), 2) THEN true ELSE false END AS is_active,
        COALESCE(COUNT(user_upload_dump_06.user_id)) AS upload_count
    FROM us
    LEFT JOIN ac ON us.id = ac.user_id
    LEFT JOIN user_upload_dump_06 ON us.id = user_upload_dump_06.user_id
    GROUP BY us.id""")
spark.sql("SELECT * FROM user_repport").show()

