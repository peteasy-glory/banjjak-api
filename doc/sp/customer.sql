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

call procPartnerPC_BeautyCutomerSearchTotal_get('pettester@peteasy.kr', 2);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_BeautyCutomerSearchTotal_get $$
CREATE PROCEDURE procPartnerPC_BeautyCutomerSearchTotal_get(
	dataPartnerId VARCHAR(64), 
    dataOrdType INT #(0: 최신순, 1: 가나다순, 2: 이용횟수별, 3:견종별, 4: 등급별)
)
BEGIN
	/**
		샵별 전체 고객 조회 (미용)
   */
   SET @ORD_STR = '';
   SET @partner_id = dataPartnerId;
   CASE WHEN dataOrdType = 1 THEN SET @ORD_STR = 'ORDER BY name ASC';
		WHEN dataOrdType = 2 THEN SET @ORD_STR = 'ORDER BY use_count ASC';
        WHEN dataOrdType = 3 THEN SET @ORD_STR = 'ORDER BY pet_type ASC';
        WHEN dataOrdType = 4 THEN SET @ORD_STR = 'ORDER BY grade DESC';
        ELSE SET @ORD_STR = 'ORDER BY AAA.ymdhm DESC';
   END CASE;

   SET @SQL_STR = CONCAT(" 
   	SELECT funcGradeOfCustomer(?, id) AS grade, AAA.* , funcUserReserve(AAA.cellphone, ?) AS reserve  
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
		) BB  ON AA.cellphone = BB.cellphone AND AA.ymdhm = BB.ymdhm
	) AAA ", @ORD_STR);
    PREPARE stmt FROM @SQL_STR;
    EXECUTE stmt USING @partner_id, @partner_id, @partner_id, @partner_id;
    DEALLOCATE PREPARE stmt;    
END $$ 
DELIMITER ;


call procPartnerPC_HotelCutomerSearchTotal_get('pettester@peteasy.kr', 2);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_HotelCutomerSearchTotal_get $$
CREATE PROCEDURE procPartnerPC_HotelCutomerSearchTotal_get(
	dataPartnerId VARCHAR(64),
     dataOrdType INT #(0: 최신순, 1: 가나다순, 2: 이용횟수별, 3:견종별, 4: 등급별)
)
BEGIN
	/**
		샵별 전체 고객 조회 (호텔)
   */
   SET @ORD_STR = '';
   SET @partner_id = dataPartnerId;
   CASE WHEN dataOrdType = 1 THEN SET @ORD_STR = 'ORDER BY name ASC';
		WHEN dataOrdType = 2 THEN SET @ORD_STR = 'ORDER BY use_count ASC';
        WHEN dataOrdType = 3 THEN SET @ORD_STR = 'ORDER BY pet_type ASC';
        WHEN dataOrdType = 4 THEN SET @ORD_STR = 'ORDER BY grade DESC';
        ELSE SET @ORD_STR = 'ORDER BY AAA.check_in_date DESC';
   END CASE;

   SET @SQL_STR = CONCAT("    
	SELECT funcGradeOfCustomer(?, id) AS grade, AAA.* , funcUserReserve(AAA.cellphone, ?) AS reserve
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
    EXECUTE stmt USING @partner_id, @partner_id, @partner_id, @partner_id;
    DEALLOCATE PREPARE stmt;    

END $$ 
DELIMITER ;

call procPartnerPC_KinderCutomerSearchTotal_get('pettester@peteasy.kr', 4);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_KinderCutomerSearchTotal_get $$
CREATE PROCEDURE procPartnerPC_KinderCutomerSearchTotal_get(
	dataPartnerId VARCHAR(64),
     dataOrdType INT #(0: 최신순, 1: 가나다순, 2: 이용횟수별, 3:견종별, 4: 등급별)
)
BEGIN
	/**
		샵별 전체 고객 조회 (유치원)
   */
   SET @ORD_STR = '';
   SET @partner_id = dataPartnerId;
   CASE WHEN dataOrdType = 1 THEN SET @ORD_STR = 'ORDER BY name ASC';
		WHEN dataOrdType = 2 THEN SET @ORD_STR = 'ORDER BY use_count ASC';
        WHEN dataOrdType = 3 THEN SET @ORD_STR = 'ORDER BY pet_type ASC';
        WHEN dataOrdType = 4 THEN SET @ORD_STR = 'ORDER BY grade DESC';
        ELSE SET @ORD_STR = 'ORDER BY AAA.check_in_date DESC';
   END CASE;

   SET @SQL_STR = CONCAT("       
	SELECT funcGradeOfCustomer(?, id) AS grade, AAA.* , funcUserReserve(AAA.cellphone, ?) AS reserve
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
    EXECUTE stmt USING @partner_id, @partner_id, @partner_id, @partner_id;
    DEALLOCATE PREPARE stmt;    

END $$ 
DELIMITER ;

call procPartnerPC_BeautyCutomerSearchTotal_get('pettester@peteasy.kr');
call procPartnerPC_HotelCutomerSearchTotal_get('pettester@peteasy.kr');
call procPartnerPC_KinderCutomerSearchTotal_get('pettester@peteasy.kr');

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



							INSERT INTO tb_tmp_user (cellphone) VALUES
							('0101010101010101010')

							INSERT INTO tb_mypet (
								tmp_seq, name, name_for_owner, type, pet_type, 
								pet_type2, year, month, day, gender, 
								neutral, weight, tmp_yn
							) VALUES (
								'150795','ttttttt','ttttttt','dog','골든리트리버',
								'','2022','1','1','남아',
								'1','5','Y'
							)
				
								INSERT INTO tb_payment_log (
									pet_seq, session_id, customer_id, order_id, artist_id,
									cellphone, etc_memo, update_time, approval, product, product_type
								) VALUES (
									'191214', '0', '신규등록(150795)', '0', 'pettester@peteasy.kr', 
									'0101010101010101010', 'dfdafdafdafd', NOW(), '0', 'ttttttt', 'A'
								)
							
									SELECT *
									FROM tb_artist_customer_list
									WHERE artist_id = 'pettester@peteasy.kr'
										AND pet_seq = '191214'
											없으면 아래 인서트 , 있으면 업데트를 한다					

										INSERT INTO tb_artist_customer_list (pet_seq, artist_id, pet_name) VALUES
										('191214', 'pettester@peteasy.kr', 'ttttttt')
                                        UPDATE tb_artist_customer_list 
                                        SET pet_name = 'ttttttt'
                                        WHERE artist_id = 'pettester@peteasy.kr'
                                                AND pet_seq = '191214'
                                        
                                        
									

loof: LOOP
		FETCH cursorPhones
			INTO aPhone;
		IF EOF THEN
			LEAVE loof;
		END IF;
        SELECT COUNT(*) INTO aNoShow
        FROM tb_payment_log 
        WHERE data_delete = 0 AND is_no_show = 1 AND cellphone = aPhone;
        SET aTotalNoShow = CONCAT(aTotalNoShow, '|', aPhone, '|', aNoShow);
        
    END LOOP;
    CLOSE cursorPhones;
    
    
    
        SELECT * 
    FROM 
    (
		SELECT cellphone, customer_id  FROM tb_payment_log 
        WHERE data_delete = 0 AND artist_id = 'sally@peteasy.kr' GROUP BY cellphone, customer_id;
        select * from tb_tmp_user where cellphone='01082320830'
	) A LEFT JOIN 
    (
		SELECT * FROM tb_customer
		WHERE enable_flag = 1 #and cellphone in ('01039091436', '01025180714', '01053906573', '01053906575', '01053906578', '01084599700')
	) B ON A.cellphone = B.cellphone;
    