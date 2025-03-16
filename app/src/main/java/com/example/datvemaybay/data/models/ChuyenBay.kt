package com.example.datvemaybay.data.models

import android.os.Parcel
import android.os.Parcelable
import com.google.gson.annotations.SerializedName
import com.google.type.DateTime
import java.io.Serializable
import java.util.Date

data class ChuyenBay(
    @SerializedName("ma_chuyen_bay") val maChuyenBay: String,
    @SerializedName("ma_hhk") val maMB: String,
    @SerializedName("hang_hang_khong") val hangHangKhong: String,
    @SerializedName("san_bay_di") val sanBayDi: String,
    @SerializedName("ma_sb_di") val maSanBayDi: String,
    @SerializedName("thoi_gian_di") val thoiGianDi: String,
    @SerializedName("san_bay_den") val sanBayDen: String,
    @SerializedName("ma_sb_den") val maSanBayDen: String,
    @SerializedName("thoi_gian_den") val thoiGianDen: String,
    @SerializedName("loai_ghe") val loaiGhe: String,
    @SerializedName("gia_ve_bus") val giaVeBus: Long,
    @SerializedName("gia_ve_eco") val giaVeEco: Long,
    @SerializedName("thoi_gian_bay") val thoiGianBay: Float,
): Serializable

data class ChuyenBayRequest(
    val san_bay_di: String,
    val san_bay_den: String,
    var ngay_di: String,
    val so_luong_khach: Int,
    val loai_ghe: String,
    val khu_hoi: Boolean,
    val ngay_ve: String,
): Serializable

data class ChuyenBayResponse(
    @SerializedName("connecting_flights") val connectingFlight: List<ChuyenBay>,
    @SerializedName("direct_flights") val directFlight: List<ChuyenBay>,
    @SerializedName("return_connecting_flights") val returnConnectingFlight: List<ChuyenBay>,
    @SerializedName("return_direct_flights") val returnDirectFlight: List<ChuyenBay>,
): Serializable