package com.example.datvemaybay.data.models

import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class KhuyenMaiResponse(
    @SerializedName("khuyen_mai") val khuyenMai: KhuyenMai,
    @SerializedName("tong_tien") val tongTien: Long
) : Serializable

data class KhuyenMai(
    @SerializedName("CHUYEN_BAY") val chuyenBay: List<Any>,
    @SerializedName("HANG_HANG_KHONG") val hangHangKhong: List<HangHangKhongKhuyenMai>
) : Serializable

data class HangHangKhongKhuyenMai(
    @SerializedName("ap_dung_cho") val apDungCho: String,
    @SerializedName("gia_tri") val giaTri: Long,
    @SerializedName("loai_khuyen_mai") val loaiKhuyenMai: String,
    @SerializedName("ma_khuyen_mai") val maKhuyenMai: String,
    @SerializedName("mo_ta") val moTa: String,
    @SerializedName("ten_khuyen_mai") val tenKhuyenMai: String,
    @SerializedName("tien_giam") val tienGiam: Long
) : Serializable

data class KhuyenMaiRequest(
    @SerializedName("hang_hang_khong") val hangHangKhong: List<String>,
    @SerializedName("ma_chuyen_bay") val maChuyenBay: List<String>,
    @SerializedName("tong_tien") val tongTien: Long
) : Serializable