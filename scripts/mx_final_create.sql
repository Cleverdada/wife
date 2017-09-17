create TABLE  mx_final as
select b.*,
case
	when b.迟到='0' AND b.早退='0' and b.旷工='0' and b.未打卡='0' then '正常' else '异常' end 类型 from

(select a.姓名, a.日期, a.上班, a.下班,
	case
		when 日期 in (select riqi from zhoumo) then 0
		when TIMESTAMPDIFF(MINUTE, CONCAT(日期,'09:30'), CONCAT(日期,上班))>60 then '>1小时'
		when TIMESTAMPDIFF(MINUTE, CONCAT(日期,'09:30'), CONCAT(日期,上班))>15 then '<=1小时'
		when TIMESTAMPDIFF(MINUTE, CONCAT(日期,'09:30'), CONCAT(日期,上班))>0 then '<=15分钟'
		else 0 END 迟到,
	case
		when 日期 in (select riqi from zhoumo) then 0
		when TIMESTAMPDIFF(MINUTE, CONCAT(日期,下班), CONCAT(日期,'18:30'))>60 then '>1小时'
		when TIMESTAMPDIFF(MINUTE, CONCAT(日期,下班), CONCAT(日期,'18:30'))>0 then '<=1小时'
		# WHEN a.下班 > '17:30' and a.下班 < '18:30' then 1
		else 0
	end 早退,

	case
		when 日期 in (select riqi from zhoumo) then 0
		when a.上班 is null or a.下班 is null then 1 else 0 end 未打卡,

	case
		when 日期 in (select riqi from zhoumo) then 1
		WHEN a.下班 >= '21:00' then 1 else 0 end 加班,
	case
		# 迟到早退1个小时以上记为旷工
		when 日期 in (select riqi from zhoumo) then 0
		when TIMESTAMPDIFF(MINUTE, CONCAT(日期,下班), CONCAT(日期,'18:30'))>60 then 1
		when TIMESTAMPDIFF(MINUTE, CONCAT(日期,'09:30'), CONCAT(日期,上班)) >60 then 1
		WHEN a.下班 < '17:30' then 1 else 0 end 旷工
 from mx_origin a) b