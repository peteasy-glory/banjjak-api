
call procPartnerPC_Setting_Artist_Working_get('eaden@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Artist_Working_get $$
CREATE PROCEDURE procPartnerPC_Setting_Artist_Working_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 미용사 근무일시 조회 
   */
	SELECT sequ_prnt, artist_id, name, nicname, if((is_main = ''or is_main = null), 0, is_main) AS is_host
		,is_out AS is_leave, is_view AS is_show
		, GROUP_CONCAT(CONCAT(seq,'|',week,'|', time_start,'|',time_end)) AS work
	FROM tb_artist_list
	WHERE artist_id = dataPartnerId
	GROUP BY name, nicname
	ORDER BY sequ_prnt ASC, seq ASC;
END $$ 
DELIMITER ;


-- call procPartnerPC_Setting_Artist_Working_get('eaden@peteasy.kr');
-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Artist_Working_get $$
-- CREATE PROCEDURE procPartnerPC_Setting_Artist_Working_get(
-- 	dataPartnerId VARCHAR(64)
-- )
-- BEGIN
-- 	/**
-- 		샵별 미용사 근무일시 조회 
--    */
-- 	SELECT * FROM tb_artist_list
-- 	WHERE artist_id = dataPartnerId;	
-- END $$ 
-- DELIMITER ;

-- 	SELECT GROUP_CONCAT(seq) AS seq, name, nicname, GROUP_CONCAT(week)
--     ,  GROUP_CONCAT(CONCAT(time_start, '-',time_end)) AS peroid, GROUP_CONCAT(sequ_prnt)
--     FROM tb_artist_list
-- 	WHERE artist_id = 'eaden@peteasy.kr'
-- 	GROUP BY name, nicname;

call procPartnerPC_Setting_Shop_OpenClose_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Shop_OpenClose_get $$
CREATE PROCEDURE procPartnerPC_Setting_Shop_OpenClose_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 오픈/글로즈 시간
   */
	select * from tb_working_schedule 
	where customer_id = dataPartnerId;
END $$ 
DELIMITER ;


call procPartnerPC_Setting_Regular_Holiday_get('eaden@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Regular_Holiday_get $$
CREATE PROCEDURE procPartnerPC_Setting_Regular_Holiday_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 정기 휴일 
   */
	select * from tb_regular_holiday 
	where customer_id = dataPartnerId;
END $$ 
DELIMITER ;


call procPartnerPC_Setting_Personal_Vacation_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Personal_Vacation_get $$
CREATE PROCEDURE procPartnerPC_Setting_Personal_Vacation_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		미용사 휴가 설정  
   */
	SELECT * FROM tb_private_holiday
    WHERE customer_id = dataPartnerId;
END $$ 
DELIMITER ;

call procPartnerPC_Setting_Time_Limit_get('eaden@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Time_Limit_get $$
CREATE PROCEDURE procPartnerPC_Setting_Time_Limit_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		타임제 설정 조회   
   */
	SELECT * FROM tb_time_schedule
    WHERE customer_id = dataPartnerId;
END $$ 
DELIMITER ;


call procPartnerPC_Setting_Break_Time_get('eaden@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Break_Time_get $$
CREATE PROCEDURE procPartnerPC_Setting_Break_Time_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		휴게시간 설정 조회   
   */
	SELECT * FROM tb_time_off
    WHERE customer_id = dataPartnerId;
END $$ 
DELIMITER ;