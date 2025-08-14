create table hive.default.t_conversion1 (
dt date,
pkg_name varchar(255),
second_channel varchar(255),
affiliate_id varchar(255),
nation varchar(255),
gaid varchar(255)
) WITH (
  external_location = 's3://pyuntestbucket1/trino/t_conversion1',
  format = 'TEXTFILE'
);


create table hive.default.t_conversion2 (
dt date,
pkg_name varchar(255),
second_channel varchar(255),
affiliate_id varchar(255),
nation varchar(255),
gaid varchar(255)
)WITH (
  external_location = 's3://pyuntestbucket1/trino/t_conversion2',
  format = 'TEXTFILE'
);


create table hive.default.t_event (
dt date,
pkg_name varchar(255),
event_name varchar(255),
second_channel varchar(255),
affiliate_id varchar(255),
nation varchar(255),
gaid varchar(255)
)WITH (
  external_location = 's3://pyuntestbucket1/trino/t_event',
  format = 'TEXTFILE'
);
