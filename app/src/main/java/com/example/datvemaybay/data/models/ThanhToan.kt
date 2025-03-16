package com.example.datvemaybay.data.models

data class PaymentData(
    val tong_tien: Long,
    val ma_khuyen_mai: String?,
    val phuong_thuc: String,
    val card_info: CardInfo?
)

data class CardInfo(
    val ngan_hang: String="",
    val so_the: String="",
    val ten_chu_the: String=""
)


data class SuccessResponse(
    val success: Boolean,
    val ma_dat_cho: List<String>,
    val ma_dat_cho_goc: String,
    val tien_giam: Double,
    val tong_tien: Double,
    val message: String
)

data class ErrorResponse(
    val error: String
)
