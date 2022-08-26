SET @id = 'pettester@peteasy.kr';
select * from tb_customer
where id = @id;

call procPartnerPC_Sales_Performance_get('pettester@peteasy.kr', '2022-08-01','2022-08-26','artist', 'pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Sales_Performance_get $$
CREATE PROCEDURE procPartnerPC_Sales_Performance_get(
	dataPartnerId VARCHAR(64),
    dataStDate VARCHAR(14),
    dataFiDate VARCHAR(14), 
	dataType VARCHAR(14),
    dataOrder VARCHAR(64)
)
BEGIN
	/**
		판매 실적
   */
	SET @partner_id = dataPartnerId;
	SET @data_st = dataStDate;
	SET @data_fi = dataFiDate;
    SET @order_str = '';
    SET @where_str = '';
    CASE 
		WHEN dataType = 'date'
		THEN
        BEGIN
			SET @order_str = ' ORDER BY A.payment_type ASC, A.reservationDate DESC';
			SET @where_str = IF(dataOrder != '', CONCAT(" AND A.payment_type = '", dataOrder,"'"), '');
		END;
		WHEN dataType = 'service'
		THEN
        BEGIN
			SET @order_str = ' ORDER BY A.service DESC';
            SET @where_str = " AND A.payment_type = '미용'";
			SET @where_str = CONCAT(@where_str, IF(dataOrder != '', CONCAT(" AND A.service = '", dataOrder,"'"), ''));
		END;
		WHEN dataType = 'artist'
		THEN
        BEGIN
			SET @order_str = ' ORDER BY A.worker DESC';
            SET @where_str = " AND A.payment_type = '미용'";
            SET @data_order = IF(dataOrder=dataPartnerID, "대표",dataOrder);
			SET @where_str = CONCAT(@where_str, IF( @data_order != '', CONCAT(" AND A.worker = '", @data_order,"'"), ''));
		END;
		WHEN dataType = 'payment'
		THEN
        BEGIN
			SET @order_str = ' ORDER BY A.payment_type DESC';
			SET @where_str = IF(dataOrder != '', CONCAT(" AND (A.pay_type = '", dataOrder, "' OR A.pay_type = '매장접수(카)')"), '');
		END;
		WHEN dataType = 'hotel'
		THEN
        BEGIN
			SET @order_str = ' ORDER BY A.room_name DESC';
            SET @where_str = " AND A.payment_type = '호텔'";
			SET @where_str = CONCAT(@where_str, IF(dataOrder != '', CONCAT(" AND A.room_name = '", dataOrder,"'"), ''));
		END; 
		WHEN dataType = 'playroom'
		THEN
        BEGIN
			SET @order_str = ' ORDER BY A.room_name DESC, A.reservation_dt ASC';
            SET @where_str = CONCAT(' AND A.payment_type = ','유치원');
			SET @where_str = CONCAT(@where_str, IF(dataOrder != '', CONCAT(" AND A.room_name = '", dataOrder,"'"), ''));
		END;
        ELSE SET @order_str = ' ORDER BY A.payment_type ASC, A.reservationDate DESC';
    END CASE;
   
   
    SET @SQL_STR = CONCAT(" 
   	SELECT *
		FROM (
			SELECT 
				  SUBSTRING_INDEX(product,'|',1) AS name			    
				, DATE_FORMAT(buy_time, '%Y-%m-%d %H:%i' ) AS reservation_dt
				, DATE_FORMAT( CONCAT( year,'-',month,'-',day,' ',hour,':',IFNULL(minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) AS reservationDate
				, DATE_FORMAT(cancel_time, '%Y-%m-%d %H:%i' ) AS cancel_dt
				, SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(product,'|',5),'|',-1), ':', 1) AS service
				, product AS extra_service
			    , payment_log_seq AS pls
			    , pl.pet_seq AS b_pet_seq
				, if(worker = ?, '대표', worker) AS worker
				, (
					case
						when pay_type = 'card' then '앱-선결제'
						when pay_type = 'bank' then '앱-선결제'
						when pay_type = 'offline-card' then '앱-매장결제'
						when pay_type = 'offline-cash' then '앱-매장결제'
						when pay_type = 'pos-card' then '매장접수'
						when pay_type = 'pos-cash' then '매장접수'
						ELSE '매장접수(카)'
					end
				) AS pay_type
                , IF(pay_type = 'card' or pay_type = 'bank', if(IFNULL(local_price, 0) + IFNULL(local_price_cash, 0) < 1,IFNULL(total_price, 0) + IFNULL(spend_point, 0) + IFNULL(add_price, 0), IFNULL(local_price, 0)),IFNULL(local_price, 0) ) AS card
				, IFNULL(local_price_cash, 0) AS cash
				, '미용' AS payment_type 
				, '' AS room_name
				, IFNULL(reserve_point, '0') AS reserve_point
				, (
					SELECT IFNULL(SUM(add_reserve), '0')
					FROM tb_user_reserve_log
					WHERE is_delete = '2'
						AND artist_id = pl.artist_id
						AND payment_log_seq = pl.payment_log_seq
						AND service_type = 'B'
						AND type = 'R'
				) AS use_reserve				
			FROM tb_payment_log AS pl
			WHERE is_cancel = 0
				AND is_no_show = 0
				AND data_delete = 0
				AND artist_id = ?
				AND DATE_FORMAT( CONCAT( year,'-',month,'-',day,' ',hour,':',IFNULL(minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) 
					BETWEEN DATE_FORMAT(CONCAT(?, ' 00:00'), '%Y-%m-%d %H:%i') 
						 AND DATE_FORMAT(CONCAT(?, ' 23:59'), '%Y-%m-%d %H:%i') 
			
			UNION all
						
			SELECT
				  mp.name
				, DATE_FORMAT(hpl.reg_dt, '%Y-%m-%d %H:%i') AS reservation_dt
				, DATE_FORMAT(CONCAT(hr.check_in_date,' ',hr.check_in_time), '%Y-%m-%d %H:%i') AS reservationDate
				, DATE_FORMAT(hpl.delete_dt, '%Y-%m-%d %H:%i') AS cancel_dt
				, CONCAT(hr.room_name,'/',TIMESTAMPDIFF(DAY,hr.check_in_date,hr.check_out_date),'박/~',hr.weight,'Kg') AS service
				, etc_product_data AS extra_service
				, '-' AS worker
				, (
					case
						when (receipt_type = 1 or receipt_type = 2) AND pay_type = 1 then '앱-선결제' 
						when (receipt_type = 1 or receipt_type = 2) AND pay_type = 2 then '앱-선결제' 
						when (receipt_type = 1 or receipt_type = 2) AND pay_type = 0 then '앱-매장결제' 
						when receipt_type = 3 then '매장접수' 
						ELSE '매장접수'
					end
				) AS pay_type
				, add_price_card AS card
				, add_price_cash AS cash
				, '호텔' AS payment_type 
				, hr.room_name AS room_name
				, '0' AS reserve_point
				, '0' AS use_reserve
				, hp_log_seq
				, hpl.pet_seq AS h_pet_seq
			FROM tb_hotel_payment_log AS hpl
				INNER JOIN tb_hotel_reservation AS hr ON hpl.order_num = hr.order_num
				INNER JOIN tb_mypet AS mp ON hpl.pet_seq = mp.pet_seq
			WHERE hpl.is_delete = '2'
				AND hpl.is_no_show = '2'
				AND hpl.data_delete = '0'
				AND hpl.artist_id = ?
				AND DATE_FORMAT(CONCAT(hr.check_in_date,' ',hr.check_in_time), '%Y-%m-%d %H:%i') 
					BETWEEN DATE_FORMAT(CONCAT(?, ' 00:00'), '%Y-%m-%d %H:%i') 
						 AND DATE_FORMAT(CONCAT(?, ' 00:00'), '%Y-%m-%d %H:%i')

			UNION all
						
			SELECT
				  mp.name
				, DATE_FORMAT(ppl.reg_dt, '%Y-%m-%d %H:%i') AS reservation_dt
				, DATE_FORMAT(CONCAT(pr.check_in_date,' ',pr.check_in_time), '%Y-%m-%d %H:%i') AS reservationDate
				, DATE_FORMAT(ppl.delete_dt, '%Y-%m-%d %H:%i') AS cancel_dt
				, IF(pr.service_type = 1, pr.allday_pass_name, CONCAT('[',pr.room_name,'h/~',pr.weight,'Kg] X ',pr.count)) AS service
				, pr.etc_product_data AS extra_service
				, '-' AS worker
				, (
					case
						when (receipt_type = 1 or receipt_type = 2) AND pay_type = 1 then '앱-선결제' 
						when (receipt_type = 1 or receipt_type = 2) AND pay_type = 2 then '앱-선결제' 
						when (receipt_type = 1 or receipt_type = 2) AND pay_type = 0 then '앱-매장결제' 
						when receipt_type = 3 then '매장접수' 
						ELSE '매장접수'
					end
				) AS pay_type
				, ppl.add_price_card AS card
				, ppl.add_price_cash AS cash
				, '유치원' AS payment_type 
				, pr.service_type AS room_name
				, '0' AS reserve_point
				, '0' AS use_reserve
				, pp_log_seq
				, ppl.pet_seq AS p_pet_seq
			FROM tb_playroom_payment_log AS ppl
				INNER JOIN tb_playroom_reservation AS pr ON ppl.order_num = pr.order_num
				INNER JOIN tb_mypet AS mp ON ppl.pet_seq = mp.pet_seq
			WHERE ppl.is_delete = '2'
				AND ppl.is_no_show = '2'
				AND ppl.data_delete = '0'
				AND ppl.artist_id = ?
				AND DATE_FORMAT(CONCAT(pr.check_in_date,' ',pr.check_in_time), '%Y-%m-%d %H:%i') 
					BETWEEN DATE_FORMAT(CONCAT(?, ' 00:00'), '%Y-%m-%d %H:%i') 
						 AND DATE_FORMAT(CONCAT(?, ' 00:00'), '%Y-%m-%d %H:%i')
		) AS A WHERE 1=1 ", @where_str, @order_str);
    PREPARE stmt FROM @SQL_STR;
    EXECUTE stmt USING @partner_id, @partner_id,@data_st, @data_fi, @partner_id, @data_st, @data_fi,@partner_id, @data_st, @data_fi;
    DEALLOCATE PREPARE stmt;    


END $$ 
DELIMITER ;


call procPartnerPC_Sales_Performance_get('pettester@peteasy.kr', '2022-08-01','2022-08-26','artist', 'pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Sales_Performance_get $$
CREATE PROCEDURE procPartnerPC_Sales_Performance_get(
	dataPets TEXT
)
BEGIN
	/**
		판매 실적 고객/동물 수
   */
   
	SELECT DISTINCT(IF(customer_id IS NULL OR customer_id = '', tmp_seq, customer_id)) AS clientID  
    FROM tb_mypet 
    WHERE pet_seq IN (dataPets); 

END $$ 
DELIMITER ;
