create or replace view 考勤明细 as
select
a.`登记号`,
a.`姓名`,
a.`部门`,
b.`日期`,
b.`上班`,
b.`下班`,
b.`迟到`,
b.`早退`,
b.`未打卡`,
b.`加班`,
b.`旷工`,
b.`类型`  from  employee a left JOIN mx_final b on a.`登记号` = b.姓名  order by CAST(a.`登记号` AS SIGNED) ASC, b.`日期` ASC;

