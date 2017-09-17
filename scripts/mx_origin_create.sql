create or replace view mx_origin as
SELECT
	case when max(b.时间) >= '12:00' then max(b.时间) ELSE null end 下班 ,
	case when min(b.时间) < '12:00' then min(b.时间) ELSE null end  上班 ,
	b.日期 ,
	b.姓名 ,
	b.all_date

FROM
	(
		SELECT
			a.姓名 ,
			substring(a.all_date , 1 , 11) 日期 ,
			substring(
				a.all_date ,
				12,5

			) 时间,
			a.all_date
		FROM
			(
				SELECT
					姓名 ,
					date_format(日期时间 , '%Y-%m-%d %H:%i:%s') all_date
				FROM
					april
			) a
	) b
GROUP BY
	b.日期 ,
	b.姓名
ORDER BY
	b.姓名;

