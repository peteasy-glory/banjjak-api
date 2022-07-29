
call procPartnerPC_Booking_BeautyPeroid_get('eaden@peteasy.kr', '2022-07-01', '2022-07-10');
#call procPartnerPC_Booking_BeautyBookingPeroid_get(\'eaden@peteasy.kr\', \'2022-07-02\', \'2022-07-20\')
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_BeautyPeroid_get $$
CREATE PROCEDURE procPartnerPC_Booking_BeautyPeroid_get(
	dataPartnerId VARCHAR(64),
    dataStDate VARCHAR(10), # format yyyy-mm-dd
    dataFiDate VARCHAR(10)  # format yyyy-mm-dd
)
BEGIN
	/**
		미용 예약 현황 기간으로 검색 
   */
   
	SELECT A.*, B.pet_seq, B.tmp_seq, B.name, B.type, B.pet_type, C.is_approve FROM 
	(
		SELECT * FROM gobeautypet.tb_payment_log 
		WHERE data_delete = 0 AND artist_id = dataPartnerId
	) A LEFT JOIN (SELECT * FROM tb_mypet WHERE data_delete = 0) B ON A.pet_seq = B.pet_seq 
    LEFT JOIN (SELECT * FROM tb_grade_reserve_approval_mgr WHERE is_delete = 0) C ON A.payment_log_seq = C.payment_log_seq
	WHERE gobeautypet.funcYMDToDate(A.year, A.month, A.day) >= dataStDate AND
		gobeautypet.funcYMDToDate(A.year, A.month, A.day) < dataFiDate;
END $$ 
DELIMITER ;