#call procPartnerPC_ShopName_get('boongdoo@naver.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_ShopName_get $$
CREATE PROCEDURE procPartnerPC_ShopName_get(
	dataArtistId VARCHAR(64)
)
BEGIN
	/**
		artist_id -> partner_id -> 샵명 가져오기 
   */
	DECLARE aPartnerId VARCHAR(128) DEFAULT '';
	DECLARE aShopName VARCHAR(128) DEFAULT '';

	SELECT customer_id INTO aPartnerId FROM tb_shop_artist
	WHERE artist_id = dataArtistId AND del_yn = 'N';
   
	IF aPartnerId = '' THEN
		SET aPartnerId = dataArtistId;
	END IF;
	
    SELECT name INTO aShopName FROM tb_shop
    WHERE customer_id = aPartnerId;
   
	SELECT aShopName;
END $$ 
DELIMITER ;

call procPartnerPC_Home_TopInfo_get('pettester@peteasy.kr', 2022, 8, 24);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_TopInfo_get $$
CREATE PROCEDURE procPartnerPC_Home_TopInfo_get(
	dataPartnerId VARCHAR(64),
    dataYear INT,    
    dataMonth INT,
    dataDay INT
)
BEGIN
	/**
		홈 메인 상단 (상당대기, 오늘일정, 신규후기, 전체고객)
   */
	DECLARE aConsulting INT DEFAULT 0;
	DECLARE aTodaySchedule INT DEFAULT 0;
	DECLARE aNewReview INT DEFAULT 0;
	DECLARE aTotalCustomer INT DEFAULT 0;
	DECLARE aShopName VARCHAR(128) DEFAULT '';
	DECLARE aNickName VARCHAR(128) DEFAULT '';
	DECLARE aFrontImage VARCHAR(128) DEFAULT '';
    DECLARE aMinus DATETIME;

    #상담 대기 건수
	SET aMinus = DATE_SUB(NOW(), INTERVAL 12 HOUR);
    SELECT COUNT(*) INTO aConsulting  
	FROM tb_payment_log A JOIN tb_customer B ON A.customer_id = B.id
	WHERE A.data_delete = 0 AND A.artist_id = dataPartnerId AND A.approval = 0 AND A.is_cancel = 0 AND A.is_no_show = 0 AND A.update_time > @aMinus;
    
    
    #오늘 일정
	SELECT COUNT(*) INTO aTodaySchedule  
	FROM tb_payment_log 
	WHERE data_delete = 0 AND artist_id = dataPartnerId AND year = dataYear  AND month = dataMonth AND day = dataDay AND is_cancel = 0 AND is_no_show = 0;            

	#신규 후기 건수
	SELECT COUNT(review_seq) INTO aNewReview
	FROM tb_usage_reviews
	WHERE artist_reply IS NULL AND is_delete = 0 AND artist_id = dataPartnerId;
    
    #샵 총 고객    
	SELECT COUNT(A.cellphone) INTO aTotalCustomer
	FROM (
		SELECT cellphone
		FROM tb_payment_log
		WHERE artist_id = dataPartnerId AND data_delete = 0 AND (cellphone != '' OR cellphone IS NOT NULL) AND (pet_seq != '' OR pet_seq != '0')
		UNION
		SELECT cellphone
		FROM tb_hotel_payment_log
		WHERE artist_id = dataPartnerId AND data_delete = 0 AND (cellphone != '' OR cellphone IS NOT NULL) AND (pet_seq != '' OR pet_seq != '0')
		UNION
		SELECT cellphone
		FROM tb_playroom_payment_log AS C
		WHERE artist_id = dataPartnerId AND data_delete = 0 AND (cellphone != '' OR cellphone IS NOT NULL) AND (pet_seq != '' OR pet_seq != '0')
	) A;
    
    #샵명
    SELECT A.name, A.front_image, B.nickname  INTO aShopName, aFrontImage, aNickName FROM tb_shop A JOIN tb_customer B ON A.customer_id = B.id  
    WHERE A.customer_id = dataPartnerId 
		AND (B.my_shop_flag = 1 or B.artist_flag = 1) and B.enable_flag = 1;
    
    SELECT aShopName, aFrontImage, aNickName, aConsulting, aTodaySchedule, aNewReview, aTotalCustomer;
END $$ 
DELIMITER ;

call procPartnerPC_Home_SpetialMall_get();
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_SpetialMall_get $$
CREATE PROCEDURE procPartnerPC_Home_SpetialMall_get(
)
BEGIN
	/**
		전문 쇼핑몰 배너 
   */
  
	SELECT A.mb_seq, A.customer_id, A.title, B.f_seq, A.odr_5, A.link, B.file_path, A.is_use_time, A.start_dt, A.end_dt
	FROM tb_main_banner A JOIN tb_file B ON A.banner = B.f_seq
	WHERE A.is_delete = 2 AND A.is_use = 1 AND A.type LIKE '%5%'
	ORDER BY A.odr_5 ASC;
END $$ 
DELIMITER ;
call procPartnerPC_Home_ConsultinMgr_get('pettester@peteasy.kr');
call procPartnerPC_Home_ConsultinMgr_get('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_ConsultinMgr_get $$
CREATE PROCEDURE procPartnerPC_Home_ConsultinMgr_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		이용 상담 관리
   */
	SELECT A.approval, A.update_time, A.payment_log_seq, C.id, C.usr_name, A.cellphone, B.pet_seq, B.name, B.pet_type
		, CONCAT(B.year,'-', LPAD(B.month,2,0),'-', LPAD(B.day,2,0)) AS birth,
        B.gender, B.neutral, B.weight, B.photo, B.beauty_exp, B.vaccination, B.bite, B.heart_trouble, B.marking, B.mounting, B.luxation, B.dermatosis
        , B.photo_counseling, A.etc_memo, CONCAT(dt_eye,dt_nose,dt_mouth,dt_ear,dt_neck,dt_body,dt_leg,dt_tail,dt_genitalia,nothing) as disliked_part 
	FROM tb_payment_log A, tb_mypet B, tb_customer C
	WHERE A.pet_seq = B.pet_seq	AND A.customer_id = C.id AND 
			A.artist_id = dataPartnerId AND A.data_delete = 0
            AND C.enable_flag = 1
	ORDER BY A.update_time DESC;
END $$ 
DELIMITER ;

call procPartnerPC_Home_ConsultingPhoto_get(5);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_ConsultingPhoto_get $$
CREATE PROCEDURE procPartnerPC_Home_ConsultingPhoto_get(
	dataPhotoCode VARCHAR(64)
)
BEGIN
	/**
		상담 포토 가져오기
   */
	#DECLARE aSQL VARCHAR(128) DEFAULT '';
	SET @aSQL = "SELECT * FROM tb_file WHERE is_delete = ? AND f_seq in(?)"; 
	PREPARE stmt FROM @aSQL;
    SET @a = 1;
    SET @b = dataPhotoCode;
	EXECUTE stmt USING @a, @b;
    DEALLOCATE PREPARE stmt;

END $$ 
DELIMITER ;


call procPartnerPC_Home_WaitingCount_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_WaitingCount_get $$
CREATE PROCEDURE procPartnerPC_Home_WaitingCount_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		승인 대기 상담, 승인 대기 예약 
   */
	DECLARE consult_waiting_num INT DEFAULT 0;
	DECLARE booking_waiting_num INT DEFAULT 0;
    
	SELECT COUNT(*) INTO consult_waiting_num #A.approval, A.update_time, A.payment_log_seq, C.id, C.usr_name, A.cellphone, B.pet_seq, B.name, B.pet_type   
	FROM tb_payment_log A, tb_mypet B, tb_customer C
	WHERE A.pet_seq = B.pet_seq	AND A.customer_id = C.id AND 
			A.artist_id = dataPartnerId AND A.data_delete = 0 AND
            C.enable_flag = 1 AND
            TIMESTAMPDIFF(minute, update_time, now()) < 720 AND
            A.approval = 0;
    
    SELECT count(*) INTO booking_waiting_num FROM tb_grade_reserve_approval_mgr a
        INNER JOIN tb_payment_log b ON a.payment_log_seq = b.payment_log_seq
        WHERE b.artist_id = dataPartnerId
        AND a.is_approve = 0;
	
    SELECT consult_waiting_num, booking_waiting_num;
END $$ 
DELIMITER ;


call procPartnerPC_Home_NoticeMgr_get(1, '2020-07-31', '2021-08-1');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_NoticeMgr_get $$
CREATE PROCEDURE procPartnerPC_Home_NoticeMgr_get(
	dataIsPeriod INT, 
	dataSt VARCHAR(10), #yyyy-mm-dd
	dataFi VARCHAR(10) #yyyy-mm-dd
)
BEGIN
	/**
		공지 사항
   */
	IF dataIsPeriod = 0 THEN
		SELECT * FROM gobeautypet.tb_admin_notice
		WHERE is_delete = 0 AND is_main = 1
		ORDER BY reg_dt DESC;
	ELSE
		SELECT * FROM gobeautypet.tb_admin_notice
		WHERE is_delete = 0 AND is_main = 1 AND
			reg_dt >= dataSt AND reg_dt < dataFi
		ORDER BY reg_dt DESC;
    END IF;
END $$ 
DELIMITER ;

call procPartnerPC_Home_BeautyBookingMgr_get('pettester@peteasy.kr', 2022, 3);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_BeautyBookingMgr_get $$
CREATE PROCEDURE procPartnerPC_Home_BeautyBookingMgr_get(
	dataPartnerId VARCHAR(64),
    dataYear INT,
    dataMonth INT
)
BEGIN
	/**
		미용 예약 현황 관리
   */
    DECLARE aYear VARCHAR(4);
    DECLARE aMonth VARCHAR(2);
	DECLARE aNextYear VARCHAR(4);
	DECLARE aNextMonth VARCHAR(2);
   
	SET aYear = CAST(dataYear AS CHAR(4));
    SET aMonth = LPAD(CAST(dataMonth AS CHAR(2)), 2, '0');
	SET aNextYear = dataYear;
	SET aNextMonth = LPAD(CAST((dataMonth+1) AS CHAR(2)), 2, '0');
    
	if dataMonth = 12 THEN
    BEGIN
		SET aNextYear = CAST((dataYear+1) AS CHAR(4));
        SET aNextMonth = 1;
    END;
    END IF;
 
	SELECT A.*, B.pet_seq, B.tmp_seq, B.name, B.type, B.pet_type, B.photo AS pet_photo, C.idx, C.is_approve FROM 
	(
		SELECT * FROM gobeautypet.tb_payment_log 
		WHERE data_delete = 0 AND artist_id = dataPartnerId
	) A LEFT JOIN (SELECT * FROM tb_mypet WHERE data_delete = 0) B ON A.pet_seq = B.pet_seq 
    LEFT JOIN (SELECT * FROM tb_grade_reserve_approval_mgr WHERE is_delete = 0) C ON A.payment_log_seq = C.payment_log_seq
	WHERE gobeautypet.funcYMDToDate(A.year, A.month, A.day) >= CONCAT(aYear, '-', aMonth, '-01') AND
		gobeautypet.funcYMDToDate(A.year, A.month, A.day) < CONCAT(aNextYear, '-', aNextMonth, '-01');
END $$ 
DELIMITER ;


call procPartnerPC_Home_HotelBookingMgr_get('choi7072@naver.com', 2022, 7);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_HotelBookingMgr_get $$
CREATE PROCEDURE procPartnerPC_Home_HotelBookingMgr_get(
	dataPartnerId VARCHAR(64),
    dataYear INT,
    dataMonth INT
)
BEGIN
	/**
		호텔 예약 현황 관리
   */
    DECLARE aYear VARCHAR(4);
    DECLARE aMonth VARCHAR(2);
	DECLARE aNextYear VARCHAR(4);
	DECLARE aNextMonth VARCHAR(2);
   
	SET aYear = CAST(dataYear AS CHAR(4));
    SET aMonth = LPAD(CAST(dataMonth AS CHAR(2)), 2, '0');
	SET aNextYear = dataYear;
	SET aNextMonth = LPAD(CAST((dataMonth+1) AS CHAR(2)), 2, '0');
    
	if dataMonth = 12 THEN
    BEGIN
		SET aNextYear = CAST((dataYear+1) AS CHAR(4));
        SET aNextMonth = 1;
    END;
    END IF;

	SELECT A.*, B.*, C.pet_seq, C.tmp_seq, C.name, C.type, C.pet_type FROM tb_hotel_payment_log A 
		JOIN tb_hotel_reservation B ON A.order_num = B.order_num
		LEFT JOIN tb_mypet C ON A.pet_seq = C.pet_seq
	WHERE A.data_delete = 0 AND B.is_delete = 2 AND A.artist_id = dataPartnerId AND
			B.check_in_date >= CONCAT(aYear, '-', aMonth, '-01') AND
			B.check_in_date < CONCAT(aNextYear, '-', aNextMonth, '-01');

END $$ 
DELIMITER ;

call procPartnerPC_Home_KindergardenBookingMgr_get('choi7072@naver.com', 2022, 7);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_KindergardenBookingMgr_get $$
CREATE PROCEDURE procPartnerPC_Home_KindergardenBookingMgr_get(
	dataPartnerId VARCHAR(64),
    dataYear INT,
    dataMonth INT
)
BEGIN
	/**
		유치원 예약 현황 관리
   */
    DECLARE aYear VARCHAR(4);
    DECLARE aMonth VARCHAR(2);
	DECLARE aNextYear VARCHAR(4);
	DECLARE aNextMonth VARCHAR(2);
   
	SET aYear = CAST(dataYear AS CHAR(4));
    SET aMonth = LPAD(CAST(dataMonth AS CHAR(2)), 2, '0');
	SET aNextYear = dataYear;
	SET aNextMonth = LPAD(CAST((dataMonth+1) AS CHAR(2)), 2, '0');
    
	if dataMonth = 12 THEN
    BEGIN
		SET aNextYear = CAST((dataYear+1) AS CHAR(4));
        SET aNextMonth = 1;
    END;
    END IF;

	SELECT A.*, B.*, C.pet_seq, C.tmp_seq, C.name, C.type, C.pet_type FROM tb_playroom_payment_log A 
		JOIN tb_playroom_reservation B ON A.order_num = B.order_num
		LEFT JOIN tb_mypet C ON A.pet_seq = C.pet_seq
	WHERE A.data_delete = 0 AND B.is_delete = 2 AND A.artist_id = dataPartnerId AND
			B.check_in_date >= CONCAT(aYear, '-', aMonth, '-01') AND
			B.check_in_date < CONCAT(aNextYear, '-', aNextMonth, '-01');

END $$ 
DELIMITER ;

-- call procPartnerPC_Home_PhoneSearch_get('eaden@peteasy.kr', '111');
call procPartnerPC_Home_PhoneSearch_get('pettester@peteasy.kr', '01053906571');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_PhoneSearch_get $$
CREATE PROCEDURE procPartnerPC_Home_PhoneSearch_get(
	dataPartnerId VARCHAR(64),
    dataPhone VARCHAR(50)
)
BEGIN
	/**
		전화번호 조회
   */
	SELECT A.*, B.name, B.type, B.pet_type, B.photo FROM
	(
		SELECT payment_log_seq, cellphone , pet_seq
		FROM tb_payment_log 
		WHERE data_delete = 0 AND artist_id = dataPartnerId AND
			cellphone LIKE CONCAT('%',dataPhone,'%') 
		GROUP BY cellphone
	 ) A LEFT JOIN tb_mypet B ON A.pet_seq = B.pet_seq;
END $$ 
DELIMITER ;

call procPartnerPC_Home_SearchPhone_get('pettester@peteasy.kr', '01053906571');
call procPartnerPC_Home_SearchPhone_get('pettester@peteasy.kr', '75');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_SearchPhone_get $$
CREATE PROCEDURE procPartnerPC_Home_SearchPhone_get(
	dataPartnerId VARCHAR(64),
    dataPhone VARCHAR(50)
)
BEGIN
	/**
		전화번호 조회
   */
	SELECT X.*, Y.family, Z.no_show_count, T.file_Path AS beauty_phoro
	FROM 
	(       
			SELECT cellphone, pet_seq, name, type, pet_type, IF(photo IS NULL, '', photo) AS pet_photo 
				#GROUP_CONCAT(client_id) AS client_id, 
				#GROUP_CONCAT(CONCAT(IF(use_date IS NULL, '', use_date),'|',pet_seq,'|',name,'|',type,'|',pet_type,'|',IF(photo IS NULL, '', photo),'|')) AS pet_info 
			FROM
			(
				SELECT A.payment_log_seq, A.pet_seq, A.cellphone, IF(A.customer_id = '' OR A.customer_id LIKE '신규등록%', B.tmp_seq, A.customer_id) AS client_id
				,CONCAT(A.year, LPAD(A.month,2,0), LPAD(A.day,2,0), LPAD(A.hour,2,0), LPAD(A.minute,2,02)) as use_date
				, C.name, C.type, C.pet_type, IF(C.photo IS NULL, '', C.photo) AS photo
				FROM tb_payment_log A 
					LEFT JOIN tb_tmp_user B ON A.cellphone = B.cellphone
					JOIN tb_mypet C ON A.pet_seq = C.pet_seq
				WHERE A.data_delete = 0 AND A.artist_id = dataPartnerId AND
					A.cellphone LIKE CONCAT('%',dataPhone,'%') 
				ORDER BY CONCAT(A.year, LPAD(A.month,2,0), LPAD(A.day,2,0), LPAD(A.hour,2,0), LPAD(A.minute,2,0)) DESC
				LIMIT 18446744073709551615
			) D  
			#WHERE use_date IS NOT NULL AND use_date != ''
			GROUP BY cellphone
			ORDER BY payment_log_seq desc

	) X	LEFT JOIN 
	(        
		SELECT to_cellphone , group_concat(from_cellphone) AS family
		FROM tb_customer_family 
		WHERE is_delete = 0 AND
			artist_id = dataPartnerId AND
			(from_cellphone like CONCAT('%',dataPhone,'%')
			OR to_cellphone like CONCAT('%',dataPhone,'%'))
		GROUP BY to_cellphone 
	) Y ON X.cellphone = Y.to_cellphone 
	 JOIN 
	(
		SELECT cellphone, SUM(is_no_show) AS no_show_count
		FROM tb_payment_log 
		WHERE data_delete = 0 AND artist_id = dataPartnerId AND
			cellphone LIKE CONCAT('%',dataPhone,'%') 
		GROUP BY cellphone
	) Z ON X.cellphone = Z.cellphone
	LEFT JOIN
	(
		SELECT * 
		FROM
		(
			SELECT * FROM tb_mypet_beauty_photo 
			WHERE artist_id = dataPhone
				AND file_path IS NOT NULL
			ORDER BY upload_dt DESC
			LIMIT 18446744073709551615
		) bp
		GROUP BY pet_seq
	) T ON X.pet_seq = T.pet_seq;
END $$ 
DELIMITER ;

call procPartnerPC_Home_FamilyPhoneSearch_get('pettester@peteasy.kr', '75');
call procPartnerPC_Home_SearchPhone_get('pettester@peteasy.kr', '777');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_FamilyPhoneSearch_get $$
CREATE PROCEDURE procPartnerPC_Home_FamilyPhoneSearch_get(
	dataPartnerId VARCHAR(64),
    dataPhone VARCHAR(50)
)
BEGIN
	/**
		전화번호 조회
   */
	SELECT *
	FROM tb_customer_family 
	WHERE is_delete = 0 AND
		artist_id = dataPartnerId AND
	    from_cellphone like CONCAT('%',dataPhone,'%')
	GROUP BY to_cellphone;
END $$ 
DELIMITER ;

  select * from tb_payment_log
  where payment_log_seq = 471352
  ;
  select * from tb_payment_log
  where cellphone = '01053900003'
  ;
call procPartnerPC_Home_SearchPetName_get('pettester@peteasy.kr', '두');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home_SearchPetName_get $$
CREATE PROCEDURE procPartnerPC_Home_SearchPetName_get(
	dataPartnerId VARCHAR(64),
    dataPetName VARCHAR(64)
)
BEGIN
    /**
		펫명 조회
   */
	SELECT X.cellphone, X.pet_seq, X.name, X.type, X.pet_type, X.pet_photo, Y.family, Z.no_show_count , T.file_path AS beauty_photo
	FROM 
	(       
		SELECT *
			#GROUP_CONCAT(client_id) AS client_id, 
			#GROUP_CONCAT(CONCAT(IF(use_date IS NULL, '', use_date),'|',pet_seq,'|',name,'|',type,'|',pet_type,'|',IF(photo IS NULL, '', photo),'|')) AS pet_info 
		FROM
		(
			SELECT A.payment_log_seq, A.pet_seq, A.cellphone, IF(A.customer_id = '' OR A.customer_id LIKE '신규등록%', B.tmp_seq, A.customer_id) AS client_id
			,CONCAT(A.year, LPAD(A.month,2,0), LPAD(A.day,2,0), LPAD(A.hour,2,0), LPAD(A.minute,2,02)) as use_date
			, C.name, C.type, C.pet_type, IF(C.photo IS NULL, '', C.photo) AS pet_photo
			FROM tb_payment_log A 
				LEFT JOIN tb_tmp_user B ON A.cellphone = B.cellphone
				JOIN tb_mypet C ON A.pet_seq = C.pet_seq
			WHERE A.data_delete = 0 AND A.artist_id = dataPartnerId AND
				(C.name LIKE CONCAT('%',dataPetName,'%') or C.pet_type LIKE CONCAT('%',dataPetName,'%'))
			ORDER BY CONCAT(A.year, LPAD(A.month,2,0), LPAD(A.day,2,0), LPAD(A.hour,2,0), LPAD(A.minute,2,0)) DESC
			LIMIT 18446744073709551615
		) D  
		#WHERE use_date IS NOT NULL AND use_date != ''
		GROUP BY cellphone, pet_seq
		ORDER BY payment_log_seq desc

	) X	LEFT JOIN 
	(        
		SELECT to_cellphone , group_concat(from_cellphone) AS family
		FROM tb_customer_family 
		WHERE is_delete = 0 AND
			artist_id = dataPartnerId
		GROUP BY to_cellphone 
	) Y ON X.cellphone = Y.to_cellphone 
	 JOIN 
	(
		SELECT cellphone, SUM(is_no_show) AS no_show_count
		FROM tb_payment_log 
		WHERE data_delete = 0 AND artist_id = dataPartnerId 
		GROUP BY cellphone
	) Z ON X.cellphone = Z.cellphone
    LEFT JOIN
	(
		SELECT * 
		FROM
		(
			SELECT * FROM tb_mypet_beauty_photo 
			WHERE artist_id = dataPartnerId 
				AND file_path IS NOT NULL
			ORDER BY upload_dt DESC
			LIMIT 18446744073709551615
		) bp
		GROUP BY pet_seq
	) T ON X.pet_seq = T.pet_seq;
    
END $$ 
DELIMITER ;

call procPartnerPC_Home__NoShowCount_get('pettester@peteasy.kr', '01089267510');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Home__NoShowCount_get $$
CREATE PROCEDURE procPartnerPC_Home__NoShowCount_get(
	dataPartnerId VARCHAR(64),
    dataPhone VARCHAR(50)
)
BEGIN
	/**
		노쇼 갯수 조회
   */
	SELECT COUNT(*)
	FROM tb_payment_log 
	WHERE data_delete = 0 AND artist_id = dataPartnerId AND
		is_no_show = 1 AND cellphone = dataPhone;

END $$ 
DELIMITER ;
-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS procPartnerPC_Home_PhoneSearch_get $$
-- CREATE PROCEDURE procPartnerPC_Home_PhoneSearch_get(
-- 	dataPartnerId VARCHAR(64),
--     dataPhone VARCHAR(50)
-- )
-- BEGIN
-- 	/**
-- 		전화번호 조회
--    */
--     DECLARE EOF INT DEFAULT FALSE;
--     DECLARE aPhone VARCHAR(20) DEFAULT '';
--     DECLARE aNoShow INT DEFAULT 0;
--     DECLARE aTotalNoShow VARCHAR(512) DEFAULT '';
--     DECLARE cursorPhones CURSOR FOR 
-- 		SELECT A.*, B.name, B.type, B.pet_type, B.photo FROM
-- 		(
-- 			SELECT payment_log_seq, cellphone , pet_seq
-- 			FROM tb_payment_log 
-- 			WHERE data_delete = 0 AND artist_id = dataPartnerId AND
-- 				cellphone LIKE CONCAT('%',dataPhone,'%') 
-- 			GROUP BY cellphone
-- 		 ) A LEFT JOIN tb_mypet B ON A.pet_seq = B.pet_seq;

-- 	DECLARE CONTINUE HANDLER FOR NOT FOUND SET EOF = TRUE;
--  	OPEN cursorPhones;
--     
--     loof: LOOP
-- 		FETCH cursorPhones
-- 			INTO aPhone;
-- 		IF EOF THEN
-- 			LEAVE loof;
-- 		END IF;
--         SELECT COUNT(*) INTO aNoShow
--         FROM tb_payment_log 
--         WHERE data_delete = 0 AND is_no_show = 1 AND cellphone = aPhone;
--         SET aTotalNoShow = CONCAT(aTotalNoShow, '|', aPhone, '|', aNoShow);
--         
--     END LOOP;
--     CLOSE cursorPhones;
-- END $$ 
-- DELIMITER ;

SELECT *
		FROM tb_customer_family 
		WHERE is_delete = 0 AND
			artist_id = 'pettester@peteasy.kr' AND
			to_cellphone ='01053906571';

SELECT * FROM
(
	SELECT cellphone , pet_seq
	FROM tb_payment_log 
	WHERE data_delete = 0 AND artist_id = 'pettester@peteasy.kr' AND
		cellphone LIKE CONCAT('%','003','%') 
	GROUP BY cellphone
 ) A LEFT JOIN tb_mypet B ON A.pet_seq = B.pet_seq   
        
 		SELECT *
		FROM tb_customer_family 
		WHERE is_delete = 0 AND
			artist_id = 'pettester@peteasy.kr' AND
			to_cellphone like CONCAT('%','3','%')
		GROUP BY from_cellphone
            
        
			LEFT JOIN tb_mypet BB ON AA.pet_seq = BB.pet_seq 
		WHERE AA.data_delete = 0 AND
			AA.artist_id = 'pettester@peteasy.kr' AND
			AA.cellphone LIKE CONCAT('%','01053906571','%')



;


/*
펫이름|
펫 종류(개,고양이)|
샵이름|
크기(소형견미용,중형견미용 등)|
미용상품(부분미용, 목욕, 위생 등)|
무게:추가요금(2:6000 => ~2kg이면 6000원)|
얼굴컷:추가요금|
미용털길이:추가요금|
털특징:추가요금(이중모:5000)|
발톱의가격(3000)|
장화의가격(4000)|
방울의가격(5000)|
미확인|
미확인|
다리추가서비스 중 선택할 갯수(기존 발톱, 장화, 방울을 선택했다면 0, 샵에 운동화컷, 구두컷 두개 상품이 추가되어있을때 하나를 선택하면 1, 두개 다 선택하면 2, 선택한 것 만큼 바로 뒤에 추가로 운동화컷:1000 추가)|
스파선택상품개수|
스파1:1000|
염색선택개수|
브릿지:3000|
기타선택개수|
기타1:3000|
제품구매수|
용품시퀀스:제품명:가격:개수(해당 카테고리에서 더 구매했다면 바로 뒤에 추가)|
간식시퀀스:제품명:가격:개수|
사료시퀀스:제품명:가격:개수|
기타제품시퀀스:제품명:가격:개수|
쿠폰구매개수|
쿠폰시퀀스:쿠폰명:가격*/
