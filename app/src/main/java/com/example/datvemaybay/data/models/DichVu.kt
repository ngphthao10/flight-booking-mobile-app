package com.example.datvemaybay.data.models

import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class DichVu(
    @SerializedName("ma_dv") val maDV: String,
    @SerializedName("ten_dich_vu") val tenDichVu: String,
    @SerializedName("mo_ta") val moTa: String,
    @SerializedName("tham_so") val thamSo: Int,
    @SerializedName("chi_tiet") val chiTiet: String
) : Serializable

data class GoiDichVu(
    @SerializedName("ma_goi") val maGoi: String,
    @SerializedName("ten_goi") val tenGoi: String,
    @SerializedName("mo_ta") val moTa: String,
    @SerializedName("gia_goi") val giaGoi: Long,
    @SerializedName("dich_vu") val dichVu: ArrayList<DichVu>
) : Serializable

data class ChuyenBayServiceResponse (
    @SerializedName("flight") val flight: ChuyenBay,
    @SerializedName("goi_dich_vu") val goiDichVu: Map<String, GoiDichVu>
) : Serializable

data class LoaiGheRequest(
    val loai_ghe: String
)

