PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
COMMIT;
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
INSERT INTO "lights_socket" VALUES(1,'Deck Lights',1,1,0,'2015-10-11 03:07:02.096951',0,'cellar','energenie');
COMMIT;
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
INSERT INTO "happenings_event" VALUES(1,'2015-06-24 05:00:01','2015-06-24 07:00:00',0,'WEEKDAY',NULL,'Temp=19','Temp=19','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(2,'2015-06-24 21:00:01','2015-06-24 22:59:59',0,'WEEKDAY',NULL,'Temp=7','Temp=7','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(4,'2015-06-24 07:00:01','2015-06-24 15:00:00',0,'WEEKDAY',NULL,'Temp=12','Temp=12','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(5,'2015-06-24 15:00:01','2015-06-24 21:00:00',0,'WEEKDAY',NULL,'Temp=19','Temp=19','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(6,'2015-06-23 23:00:01','2015-06-24 05:00:00',0,'WEEKDAY',NULL,'Temp=7','Temp=7','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(7,'2015-06-26 23:00:01','2015-06-27 05:00:00',0,'WEEKLY',NULL,'Temp=7','Temp=7','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(8,'2015-06-27 05:00:01','2015-06-27 09:00:00',0,'WEEKLY',NULL,'Temp=19','Temp=19','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(9,'2015-06-27 09:00:01','2015-06-27 15:00:00',0,'WEEKLY',NULL,'Temp=15','Temp=15','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(10,'2015-06-27 15:00:01','2015-06-27 22:00:00',0,'WEEKLY',NULL,'Temp=19','Temp=19','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(11,'2015-06-27 22:00:01','2015-06-27 22:59:59',0,'WEEKLY',NULL,'Temp=7','Temp=7','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(12,'2015-06-27 23:00:01','2015-06-28 05:00:00',0,'WEEKLY',NULL,'Temp=7','Temp=7','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(13,'2015-06-28 05:00:01','2015-06-28 09:00:00',0,'WEEKLY',NULL,'Temp=19','Temp=19','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(14,'2015-06-28 09:00:01','2015-06-28 15:00:00',0,'WEEKLY',NULL,'Temp=15','Temp=15','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(15,'2015-06-28 15:00:01','2015-06-28 22:00:00',0,'WEEKLY',NULL,'Temp=19','Temp=19','eeeeee','','000000','',1);
INSERT INTO "happenings_event" VALUES(16,'2015-06-28 22:00:01','2015-06-28 22:59:59',0,'WEEKLY',NULL,'Temp=7','Temp=7','eeeeee','','000000','',1);
COMMIT;
