SET @count = 0;
call procPartnerPC_CustomerTotalCount_get('pettester@peteasy.kr');
SELECT @count;
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_CustomerTotalCount_get $$
CREATE PROCEDURE procPartnerPC_CustomerTotalCount_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 전체 고객 수
   */
	SET @customer_count = 0;
	SELECT COUNT(*) INTO @customer_count
	FROM
	(
		(
			SELECT cellphone 
			FROM tb_payment_log
			WHERE data_delete = 0 AND artist_id = dataPartnerId
			GROUP BY cellphone
		)
		UNION
		(
			SELECT cellphone
			FROM tb_hotel_payment_log
			WHERE is_delete = 2 AND artist_id = dataPartnerId
			GROUP BY cellphone
		)
		UNION
		(
			SELECT cellphone
			FROM tb_playroom_payment_log
			WHERE is_delete = 2 AND artist_id = dataPartnerId
			GROUP BY cellphone
		)
	) A;
    
    #SET outCount = @customer_count;
	SELECT @customer_count AS count;
END $$ 
DELIMITER ;

call procPartnerPC_AnimalTotalCount_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_AnimalTotalCount_get $$
CREATE PROCEDURE procPartnerPC_AnimalTotalCount_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 전체 동물 수
   */
	SET @animal_count = 0;
	SELECT COUNT(*) INTO @animal_count
	FROM
	(
		(
			SELECT pet_seq 
			FROM tb_payment_log
			WHERE data_delete = 0 AND artist_id = dataPartnerId
			GROUP BY pet_seq
		)
		UNION
		(
			SELECT pet_seq
			FROM tb_hotel_payment_log
			WHERE is_delete = 2 AND artist_id = dataPartnerId
			GROUP BY pet_seq
		)
		UNION
		(
			SELECT pet_seq
			FROM tb_playroom_payment_log
			WHERE is_delete = 2 AND artist_id = dataPartnerId
			GROUP BY pet_seq
		)
	) A;
    
    #SET @outCount = @animal_count;
	SELECT @animal_count AS count;
    
END $$ 
DELIMITER ;



call procPartnerPC_GradeOrdAndName('pettester@peteasy.kr','saychanjin@naver.com',@grade_ord, @grade_name);
select @grade_ord, @grade_name;
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_GradeOrdAndName $$
CREATE PROCEDURE procPartnerPC_GradeOrdAndName(
	dataPartnerId VARCHAR(64),
    dataCustomerId VARCHAR(64),
    OUT outGradeOrd INT,
	OUT outGradeName VARCHAR(64)
)BEGIN
	/**
		샵내 고객 등급, 순위 
   */

	SET @grade_name = '';
	SET @grade_ord = 0;
	SELECT A.grade_name, A.grade_ord INTO @grade_name , @grade_ord
    FROM tb_grade_of_shop A JOIN tb_grade_of_customer B
		ON A.idx = B.grade_idx
    WHERE A.artist_id = dataPartnerId AND A.is_delete = 0
			AND B.customer_id = dataCustomerId;

    SET outGradeOrd = @grade_ord;
    SET outGradeName = @grade_name;
   
END $$ 
DELIMITER ;

call procPartnerPC_BeautyCutomerSearchTotal_get('pettester@peteasy.kr', 0, 10, 10);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_BeautyCutomerSearchTotal_get $$
CREATE PROCEDURE procPartnerPC_BeautyCutomerSearchTotal_get(
	dataPartnerId VARCHAR(64), 
    dataOrdType INT, #(0: 최신순, 1: 가나다순, 2: 이용횟수별, 3:견종별, 4: 등급별)
    dataStart INT,
    dataNum INT
)
BEGIN
	/**
		샵별 전체 고객 조회 (미용)
   */
   SET @ORD_STR = '';
   SET @partner_id = dataPartnerId;
   SET @data_start = dataStart-1;
   SET @data_num = dataNum;
   CASE WHEN dataOrdType = 1 THEN SET @ORD_STR = 'ORDER BY name ASC LIMIT ?, ?';
		WHEN dataOrdType = 2 THEN SET @ORD_STR = 'ORDER BY use_count ASC LIMIT ?, ?';
        WHEN dataOrdType = 3 THEN SET @ORD_STR = 'ORDER BY pet_type ASC LIMIT ?, ?';
        WHEN dataOrdType = 4 THEN SET @ORD_STR = 'ORDER BY grade DESC LIMIT ?, ?';
        ELSE SET @ORD_STR = 'ORDER BY AAA.ymdhm DESC  LIMIT ?, ?';
   END CASE;

   SET @SQL_STR = CONCAT(" 
   	SELECT funcGradeInfoOfCustomer(?, id) AS grade, AAA.* , funcUserReserve(AAA.cellphone, ?) AS reserve  
	FROM (SELECT @num:=0) NUM_T , (
		SELECT AA.*, IF((LENGTH(BB.customer_id) > 0 ), BB.customer_id, funcTmpUserIndex(AA.cellphone)) AS id,
		BB.pet_seq, BB.name, BB.pet_type, BB.type, BB.product
		FROM (
			SELECT cellphone, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) AS ymdhm
					, COUNT(case when product_type='B' then 1 end) AS use_count
					, SUM(IFNULL(local_price,0)+IFNULL(total_price,0)) AS sum_card 
					, SUM(IFNULL(local_price_cash, 0)) AS sum_cash 
			FROM tb_payment_log 
			WHERE data_delete = 0 AND artist_id = ?
			GROUP BY cellphone
		) AA LEFT JOIN  
		(
			SELECT A.*, B.name, B.pet_type, B.type, CONCAT(A.year,LPAD(A.month,2,0),LPAD(A.day,2,0),LPAD(A.hour,2,0),LPAD(A.minute,2,0)) AS ymdhm
			FROM tb_payment_log A JOIN tb_mypet B ON A.pet_seq = B.pet_seq  
			WHERE A.data_delete = 0 AND A.artist_id = ?
				AND A.is_cancel = 0 AND A.is_no_show = 0
		) BB  ON AA.cellphone = BB.cellphone 
	) AAA ", @ORD_STR);#AND AA.ymdhm = BB.ymdhm
    PREPARE stmt FROM @SQL_STR;
    EXECUTE stmt USING @partner_id, @partner_id, @partner_id, @partner_id, @data_start, @data_num;
    DEALLOCATE PREPARE stmt;    
END $$ 
DELIMITER ;


call procPartnerPC_HotelCutomerSearchTotal_get('pettester@peteasy.kr', 2);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_HotelCutomerSearchTotal_get $$
CREATE PROCEDURE procPartnerPC_HotelCutomerSearchTotal_get(
	dataPartnerId VARCHAR(64),
    dataOrdType INT, #(0: 최신순, 1: 가나다순, 2: 이용횟수별, 3:견종별, 4: 등급별)
    dataStart INT,
    dataNum INT
)
BEGIN
	/**
		샵별 전체 고객 조회 (호텔)
   */
   SET @ORD_STR = '';
   SET @partner_id = dataPartnerId;
   SET @data_start = dataStart-1;
   SET @data_num = dataNum;
   CASE WHEN dataOrdType = 1 THEN SET @ORD_STR = 'ORDER BY name ASC LIMIT ?, ?';
		WHEN dataOrdType = 2 THEN SET @ORD_STR = 'ORDER BY use_count ASC LIMIT ?, ?';
        WHEN dataOrdType = 3 THEN SET @ORD_STR = 'ORDER BY pet_type ASC LIMIT ?, ?';
        WHEN dataOrdType = 4 THEN SET @ORD_STR = 'ORDER BY grade DESC LIMIT ?, ?';
        ELSE SET @ORD_STR = 'ORDER BY AAA.check_in_date DESC LIMIT ?, ?';
   END CASE;

   SET @SQL_STR = CONCAT("    
	SELECT funcGradeInfoOfCustomer(?, id) AS grade, AAA.* , funcUserReserve(AAA.cellphone, ?) AS reserve
	FROM(
		SELECT AA.cellphone, AA.use_count, AA.check_in_date, AA.sum_card, AA.sum_cash, BB.id, BB.pet_seq, BB.name, BB.type, BB.pet_type 
		FROM (
			SELECT A.cellphone, MAX(CONCAT(B.check_in_date, ' ', B.check_in_time)) AS check_in_date
				, COUNT(case when LENGTH(A.order_num)>0 then 1 end) AS use_count
				, SUM(IFNULL(A.add_price_card, 0)) AS sum_card
				, SUM(IFNULL(A.add_price_cash, 0)) AS sum_cash
			FROM tb_hotel_payment_log A JOIN tb_hotel_reservation B ON A.order_num = B.order_num
			WHERE A.is_delete = 2 AND A.artist_id = ? AND B.is_delete = 2
			GROUP BY A.cellphone
		) AA LEFT JOIN (
			SELECT A.cellphone, IF(LENGTH(A.customer_id) > 0, A.customer_id, A.tmp_seq) AS id 
					, CONCAT(B.check_in_date, ' ', B.check_in_time) AS check_in_date
					, C.pet_seq, C.name, C.pet_type, C.type
			FROM tb_hotel_payment_log A JOIN tb_hotel_reservation B ON A.order_num = B.order_num
				JOIN tb_mypet C ON A.pet_seq = C.pet_seq
			WHERE A.is_delete = 2 AND A.artist_id = ? AND B.is_delete = 2
		) BB ON AA.cellphone = BB.cellphone AND AA.check_in_date = BB.check_in_date
	) AAA ", @ORD_STR);
    PREPARE stmt FROM @SQL_STR;
    EXECUTE stmt USING @partner_id, @partner_id, @partner_id, @partner_id, @data_start, @data_num;
    DEALLOCATE PREPARE stmt;    

END $$ 
DELIMITER ;

call procPartnerPC_KinderCutomerSearchTotal_get('pettester@peteasy.kr', 4);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_KinderCutomerSearchTotal_get $$
CREATE PROCEDURE procPartnerPC_KinderCutomerSearchTotal_get(
	dataPartnerId VARCHAR(64),
     dataOrdType INT, #(0: 최신순, 1: 가나다순, 2: 이용횟수별, 3:견종별, 4: 등급별)
    dataStart INT,
    dataNum INT
)
BEGIN
	/**
		샵별 전체 고객 조회 (유치원)
   */
   SET @ORD_STR = '';
   SET @partner_id = dataPartnerId;
   SET @data_start = dataStart-1;
   SET @data_num = dataNum;
   CASE WHEN dataOrdType = 1 THEN SET @ORD_STR = 'ORDER BY name ASC LIMIT ?, ?';
		WHEN dataOrdType = 2 THEN SET @ORD_STR = 'ORDER BY use_count ASC LIMIT ?, ?';
        WHEN dataOrdType = 3 THEN SET @ORD_STR = 'ORDER BY pet_type ASC LIMIT ?, ?';
        WHEN dataOrdType = 4 THEN SET @ORD_STR = 'ORDER BY grade DESC LIMIT ?, ?';
        ELSE SET @ORD_STR = 'ORDER BY AAA.check_in_date DESC LIMIT ?, ?';
   END CASE;

   SET @SQL_STR = CONCAT("       
	SELECT funcGradeInfoOfCustomer(?, id) AS grade, AAA.* , funcUserReserve(AAA.cellphone, ?) AS reserve
	FROM(
		SELECT AA.cellphone, AA.use_count, AA.check_in_date, AA.sum_card, AA.sum_cash, BB.id, BB.pet_seq, BB.name, BB.type, BB.pet_type 
		FROM (
			SELECT A.cellphone, MAX(CONCAT(B.check_in_date, ' ', B.check_in_time)) AS check_in_date
				, COUNT(case when LENGTH(A.order_num)>0 then 1 end) AS use_count
				, SUM(IFNULL(A.add_price_card, 0)) AS sum_card
				, SUM(IFNULL(A.add_price_cash, 0)) AS sum_cash
			FROM tb_playroom_payment_log A JOIN tb_playroom_reservation B ON A.order_num = B.order_num
			WHERE A.is_delete = 2 AND A.artist_id = ? AND B.is_delete = 2
			GROUP BY A.cellphone
		) AA LEFT JOIN (
			SELECT A.cellphone, IF(LENGTH(A.customer_id) > 0, A.customer_id, A.tmp_seq) AS id 
					, CONCAT(B.check_in_date, ' ', B.check_in_time) AS check_in_date
					, C.pet_seq, C.name, C.pet_type, C.type
			FROM tb_playroom_payment_log A JOIN tb_playroom_reservation B ON A.order_num = B.order_num
				JOIN tb_mypet C ON A.pet_seq = C.pet_seq
			WHERE A.is_delete = 2 AND A.artist_id = ? AND B.is_delete = 2
		) BB ON AA.cellphone = BB.cellphone AND AA.check_in_date = BB.check_in_date
	) AAA ", @ORD_STR);
    PREPARE stmt FROM @SQL_STR;
    EXECUTE stmt USING @partner_id, @partner_id, @partner_id, @partner_id, @data_start, @data_num;
    DEALLOCATE PREPARE stmt;    

END $$ 
DELIMITER ;

#==========================================================================
call procPartnerPC_BeautyAgree_get('pettester@peteasy.kr', 178430);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_BeautyAgree_get $$
CREATE PROCEDURE procPartnerPC_BeautyAgree_get(
	dataPartnerId VARCHAR(64),
    dataPetIdx INT
)
BEGIN
	/**
		샵 펫별 미용 동의서 
   */
	SELECT A.* , B.image
    FROM tb_beauty_agree A LEFT JOIN tb_beauty_sign B ON A.bs_seq = B.bs_seq
	WHERE artist_id = dataPartnerId AND pet_id = dataPetIdx
	;
END $$ 
DELIMITER ;
select * from tb_mypet order by pet_seq desc;
#=========================================================================
call procPartnerPC_CustomerJoin_post('pettester@peteasy.kr', '1103202032020',
'petName', 'dog', '골든리트리버', 2022, 1, 1, '남아', '0', '2.4','2회','1회','안해요','없음','0','0','0','0','it is memo');
select * from tb_tmp_user order by tmp_seq desc;
select * from tb_payment_log order by payment_log_seq desc;
select * from tb_mypet order by  pet_seq desc;
select * from  tb_artist_customer_list order by ac_seq desc;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_CustomerJoin_post $$
CREATE PROCEDURE procPartnerPC_CustomerJoin_post(
	dataPartnerId VARCHAR(64),    
    dataCellphone VARCHAR(24),    
    dataName VARCHAR(64),    
    dataType VARCHAR(8),    
    dataPetType VARCHAR(32),    
    dataYear INT,    
    dataMonth INT,    
    dataDay INT,    
    dataGender VARCHAR(10),    
    dataWNeutral VARCHAR(1),    
    dataWeight VARCHAR(10),    
    dataBeautyExp VARCHAR(10),    
    dataVaccination VARCHAR(10),    
    dataBite VARCHAR(10),    
    dataLuxation VARCHAR(10),    
    dataDermatosis VARCHAR(1),    
    dataHeartTrouble VARCHAR(1),    
    dataMarking VARCHAR(1),    
    dataMounting VARCHAR(1),    
    dataMemo TEXT
)
BEGIN
	/**
		샵 신규 고객 등록
   */
	DECLARE aErr INT DEFAULT '0';
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SET @tmp_idx = 0;
    SET @pet_idx = 0;
    
	SELECT tmp_seq INTO @tmp_idx 
    FROM tb_tmp_user 
    WHERE cellphone = dataCellphone;
        
	START TRANSACTION;   

    IF @tmp_idx < 1 THEN 
    BEGIN
		INSERT INTO tb_tmp_user (cellphone) VALUES (dataCellphone);
        SET @tmp_idx = LAST_INSERT_ID();
	END;
    END IF;

    INSERT INTO tb_mypet(tmp_seq, name, name_for_owner, type, pet_type, 
								pet_type2, year, month, day, gender, 
								neutral, weight, tmp_yn, 
                                beauty_exp, vaccination, bite, luxation, dermatosis, heart_trouble, marking, mounting)
					values(@tmp_idx, dataName, dataName, dataType, dataPetType, '' , dataYear, dataMonth, dataDay, dataGender, dataWNeutral, dataWeight, 'Y',
							dataBeautyExp, dataVaccination, dataBite, dataLuxation, dataDermatosis, dataHeartTrouble, dataMarking, dataMounting);
	SET @pet_idx = LAST_INSERT_ID();
    INSERT INTO tb_payment_log (pet_seq, session_id, customer_id, order_id, artist_id, cellphone, etc_memo, update_time, approval, product, product_type)
				VALUES (@pet_idx, '0', CONCAT('신규등록(',@tmp_idx,')'), '0', dataPartnerId, dataCellphone, dataMemo, NOW(), '0', dataName, 'A');
                 
	SET @count = 0;
   	SELECT COUNT(*) INTO @count
	FROM tb_artist_customer_list
	WHERE artist_id = dataPartnerId AND pet_seq = @pet_idx;
    
    IF @count > 0 THEN
		UPDATE tb_artist_customer_list SET pet_name = dataName WHERE artist_id = dataPartnerId AND pet_seq = @pet_idx;
    ELSE
		INSERT tb_artist_customer_list (pet_seq, artist_id, pet_name) VALUES (@pet_idx, dataPartnerId, dataName);
    END IF;
                
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;

	SELECT aErr AS err;

END $$ 
DELIMITER ;


call procPartnerPC_BeautyUsageHistory_get('pettester@peteasy.kr', '01053906571');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_BeautyUsageHistory_get $$
CREATE PROCEDURE procPartnerPC_BeautyUsageHistory_get(
	dataPartnerId VARCHAR(64),
    dataPhone VARCHAR(20)
)
BEGIN
	/**
	 최근 이용 내역 
   */
	SELECT * FROM tb_payment_log 
	WHERE cellphone = dataPhone AND artist_id = dataPartnerId
	AND is_no_show = 0 AND is_cancel = 0 AND approval = 1 
	ORDER BY CONCAT(year, LPAD(month,2,0), LPAD(day,2,0), LPAD(hour,2,0), LPAD(minute,2,0)) DESC;
    
END $$ 
DELIMITER ;

call procPartnerPC_PetList_get('pettester@peteasy.kr', '01053906572');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_PetList_get $$
CREATE PROCEDURE procPartnerPC_PetList_get(
	dataPartnerId VARCHAR(64),
    dataPhone VARCHAR(20)
)
BEGIN
	/**
	 펫 종류 
   */
	SELECT B.*
	FROM tb_payment_log A JOIN tb_mypet B 
		ON A.pet_seq = B.pet_seq
	WHERE A.data_delete = 0 AND B.data_delete = 0
		AND A.cellphone = dataPhone AND A.artist_id = dataPartnerId
	GROUP BY A.pet_seq;
    
END $$ 
DELIMITER ;

call procPartnerPC_UniqueMemo_get('pettester@peteasy.kr', '01089267510');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_UniqueMemo_get $$
CREATE PROCEDURE procPartnerPC_UniqueMemo_get(
	dataPartnerId VARCHAR(64),
    dataPhone VARCHAR(20)
)
BEGIN
	/**
	 특이 사항 최근순 
   */
	SELECT CONCAT(year,'.', LPAD(month,2,0),'.', LPAD(day,2,0)) AS recent, etc_memo
	FROM tb_payment_log 
	WHERE cellphone = dataPhone AND artist_id = dataPartnerId
		AND is_no_show = 0 AND is_cancel = 0 AND approval = 1 
		AND etc_memo != '';
    
END $$ 
DELIMITER ;


call procPartnerPC_Reserves_get(592111, '',152634,'B','U');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Reserves_get $$
CREATE PROCEDURE procPartnerPC_Reserves_get(
	dataPaymentIdx INT,
    dataCustomerID VARCHAR(64),
    dataTmpUserIdx INT,
    dataService CHAR(1),
    dataReserveType CHAR(1)
)
BEGIN
	/**
	 구매별 사용 적립금/ 이후 누적금 
   */
	SET @use_reserve = 0;
    SET @reserve = 0;
    
	IF dataCustomerID != '' THEN
		SELECT use_reserve, now_reserve INTO @use_reserve, @accum_reserve
		FROM tb_user_reserve_log 
		WHERE payment_log_seq = dataPaymentIdx AND service_type = dataService AND type = dataReserveType AND customer_id = dataCustomerID;
    ELSE
		SELECT use_reserve, now_reserve INTO @use_reserve, @accum_reserve
		FROM tb_user_reserve_log 
		WHERE payment_log_seq = dataPaymentIdx AND service_type = dataService AND type = dataReserveType AND tmp_seq = dataTmpUserIdx;
    END IF;
    
    SELECT @use_reserve AS use_reserve , @reserve AS accum_reserve;
END $$ 
DELIMITER ;

call procPartnerPC_Pet_delete('pettester@peteasy.kr', 146693);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Pet_delete $$
CREATE PROCEDURE procPartnerPC_Pet_delete(
	dataPartnerId VARCHAR(64),
    dataPetIdx INT
)
BEGIN
	/**
	 펫 삭제(페이먼트 내역만 삭제됨)
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    START TRANSACTION;
    
	UPDATE tb_payment_log   
    SET data_delete = '1'
	WHERE pet_seq = dataPetIdx AND artist_id = dataPartnerId;
	
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

call procPartnerPC_Customer_delete('pettester@peteasy.kr', 3333);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Customer_delete $$
CREATE PROCEDURE procPartnerPC_Customer_delete(
	dataPartnerId VARCHAR(64),
    dataCellPhone VARCHAR(20)
)
BEGIN
	/**
	 고객 삭제(페이먼트 내역만 삭제됨)
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    START TRANSACTION;
    
	UPDATE tb_payment_log   
    SET data_delete = '1'
	WHERE cellphone = dataCellPhone AND artist_id = dataPartnerId;

	UPDATE tb_hotel_payment_log   
    SET data_delete = '1'
	WHERE cellphone = dataCellPhone AND artist_id = dataPartnerId;

	UPDATE tb_playroom_payment_log   
    SET data_delete = '1'
	WHERE cellphone = dataCellPhone AND artist_id = dataPartnerId;
	
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

select * from tb_tmp_user
order by tmp_seq desc;

select * from tb_payment_log
where artist_id = 'pettester@peteasy.kr'
order by payment_log_seq desc
;

call procPartnerPC_Customer_SubPhone_get('pettester@peteasy.kr', '01056785608');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Customer_SubPhone_get $$
CREATE PROCEDURE procPartnerPC_Customer_SubPhone_get(
	dataPartnerID VARCHAR(64),
    dataMainPhone VARCHAR(32)
)
BEGIN
	/**
	보조 연락처 조회
   */
	SET @client_id = '';
		
	SELECT customer_id INTO @client_id 
	FROM tb_payment_log 
	WHERE artist_id = dataPartnerID AND cellphone = dataMainPhone
	GROUP BY cellphone;

	IF @client_id IS NULL OR @client_id = '' THEN
		SELECT customer_id INTO @client_id 
		FROM tb_playroom_payment_log 
		WHERE artist_id = dataPartnerID AND cellphone = dataMainPhone
		GROUP BY cellphone;
    END IF;
    
    IF @client_id IS NULL OR @client_id = '' THEN
		SELECT customer_id INTO @client_id 
		FROM tb_hotel_payment_log 
		WHERE artist_id = dataPartnerID AND cellphone = dataMainPhone
		GROUP BY cellphone;
    END IF;

	IF @client_id IS NULL OR @client_id = '' THEN
		SELECT CONCAT(tmp_seq) INTO @client_id
        FROM tb_tmp_user
        WHERE cellphone = dataMainPhone LIMIT 1;
	END IF;
    
    
	SELECT * , @client_id AS client_id
	FROM tb_customer_family 
	WHERE artist_id = dataPartnerID 
		AND to_cellphone = dataMainPhone AND is_delete = 0;
END $$ 
DELIMITER ;

call procPartnerPC_Customer_SubPhone_post('pettester@peteasy.kr', '01089267510','hptop sub', '01989267510');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Customer_SubPhone_post $$
CREATE PROCEDURE procPartnerPC_Customer_SubPhone_post(
	dataPartnerID VARCHAR(64),
    dataMainPhone VARCHAR(32),
    dataSubName VARCHAR(64),
	dataSubPhone VARCHAR(32)
)
BODY: BEGIN
	/**
	보조 연락처 추가
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    SET @cnt = -1;
    SET @idx = -1;
	SELECT is_delete, family_seq INTO @cnt, @idx 
	FROM tb_customer_family 
	WHERE artist_id = dataPartnerID
		AND to_cellphone = dataMainPhone AND from_cellphone = dataSubPhone;
	
    IF @cnt = 0 THEN
    BEGIN
		SELECT 906 as err; 
		LEAVE BODY;
    END;
    END IF;


	START TRANSACTION;

	IF @cnt < 0 THEN
		INSERT INTO tb_customer_family 
		SET artist_id      = dataPartnerID, 
		to_cellphone       = dataMainPhone, 
		to_customer_id     = '', 
		from_nickname      = dataSubName,
		from_cellphone     = dataSubPhone, 
		from_customer_id   = '', 
		reg_dt             = NOW();   
	ELSE
		UPDATE tb_customer_family 
        SET is_delete = 0,from_nickname = dataSubName  
WHERE family_seq = @idx;  
	END IF;
    
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
    
	SELECT aErr as err;
END $$ 
DELIMITER ;

call procPartnerPC_Customer_SubPhone_put('pettester@peteasy.kr', '01089267510','hptop sub', '01989267510');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Customer_SubPhone_put $$
CREATE PROCEDURE procPartnerPC_Customer_SubPhone_put(
	dataSubPhoneIdx INT
)
BODY: BEGIN
	/**
	보조 연락처 수정
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
	START TRANSACTION;

	UPDATE tb_customer_family SET is_delete = 1 WHERE family_seq = dataSubPhoneIdx;  

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	SELECT aErr as err;
END $$ 
DELIMITER ;

call procPartnerPC_Customer_RepresentativePhoneHistory_get('pettester@peteasy.kr', '');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Customer_RepresentativePhoneHistory_get $$
CREATE PROCEDURE procPartnerPC_Customer_RepresentativePhoneHistory_get(
	dataPartnerID VARCHAR(64),
    dataCustomerID VARCHAR(64)
)
BEGIN 
	/**
		대표전화 이력 조회(파트너샵)
   */
	
    IF dataCustomerID = '' THEN
		SELECT * 
		FROM tb_representative_phone_modify_history
		WHERE partner_id=dataPartnerID;
    ELSE
		SELECT * 
		FROM tb_representative_phone_modify_history
		WHERE partner_id = dataPartnerID AND customer_id = dataCustomerID;
    END IF;
	
END $$ 
DELIMITER ;

call procPartnerPC_Booking_RepresentativePhoneHistory_post('pettester@peteasy.kr', '',96992,'0312022022','01056785608');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Customer_RepresentativePhoneHistory_post $$
CREATE PROCEDURE procPartnerPC_Customer_RepresentativePhoneHistory_post(
	dataPartnerID VARCHAR(64),
	dataCustomerID VARCHAR(64),
    dataTmpUserIdx INT,
	dataOldPhone VARCHAR(20),
	dataNewPhone VARCHAR(20)
)
BODY:BEGIN
	/**
		대표전화 변경 이력 추가(파트너샵에서)
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

    START TRANSACTION;
    
	IF dataTmpUserIdx > 0 AND dataCustomerID = '' THEN
    BEGIN
		SET @cnt = 0;
        SELECT COUNT(*) INTO @cnt
        FROM tb_tmp_user
        WHERE cellphone = dataOldPhone 
			AND tmp_seq = dataTmpUserIdx; 
        IF @cnt < 1 THEN
		BEGIN	
			SELECT 907 AS err;
			LEAVE BODY;
        END;
        END IF;
    
		INSERT INTO tb_representative_phone_modify_history(partner_id, customer_id, old_phone, new_phone)
		VALUES (dataPartnerID, CONCAT(dataTmpUserIdx), dataOldPhone, dataNewPhone);
    
        UPDATE tb_customer_family 
        SET to_cellphone = dataNewPhone,
			from_cellphone = dataOldPhone
        WHERE artist_id = dataPartnerID
			AND to_cellphone = dataOldPhone
            AND from_cellphone = dataNewPhone;

        UPDATE tb_customer_family 
        SET to_cellphone = dataNewPhone
        WHERE artist_id = dataPartnerID
			AND to_cellphone = dataOldPhone;
            
		UPDATE tb_tmp_user 
		SET cellphone = dataNewPhone
		WHERE cellphone = dataOldPhone;
        
        UPDATE tb_payment_log
        SET cellphone = dataNewPhone
        WHERE artist_id = dataPartnerID
			AND customer_id = '' AND cellphone = dataOldPhone;

        UPDATE tb_playroom_payment_log 
        SET cellphone = dataNewPhone
        WHERE artist_id = dataPartnerID
			AND customer_id = '' AND cellphone = dataOldPhone;

        UPDATE tb_hotel_payment_log 
        SET cellphone = dataNewPhone
        WHERE artist_id = dataPartnerID
			AND customer_id = '' AND cellphone = dataOldPhone;
    END;
    END IF;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
END $$ 
DELIMITER ;


					select cellphone from  tb_payment_log
						where data_delete = 0 and etc_memo != '' and artist_id = 'pettester@peteasy.kr';
                        
					WHERE a.cellphone = '010892675101' AND a.artist_id = 'pettester@peteasy.kr'
					
					
				

				
select * From tb_mypet where pet_seq = 167426;


-- 정회원 여부
select * from tb_customer where cellphone = '01084797510' and nickname not like 'cellp_%'
-- 가회원 여부
select * from tb_tmp_user where cellphone = '01084797510'

SELECT * FROM tb_customer WHERE cellphone = '01084797510' and nickname not like 'cellp_%'

SELECT * FROM tb_tmp_user WHERE cellphone = '01084797510'

SELECT COUNT(*) AS cnt, name FROM tb_mypet WHERE customer_id = '' AND tmp_seq = '152634'


select * from tb_customer_family where 
	artist_id = 'pettester@peteasy.kr'  and  to_cellphone = '31053906571'
    and (
 to_cellphone = '01089267510' or from_cellphone = '01089267510');

select cellphone from tb_payment_log 
where artist_id = 'pettester@peteasy.kr'  and  customer_id = ''







