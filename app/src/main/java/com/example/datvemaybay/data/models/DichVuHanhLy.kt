package com.example.datvemaybay.data.models

import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class DichVuHanhLy(
    @SerializedName("gia") val price: Long,
    @SerializedName("ma_dich_vu") val serviceId: Int,
    @SerializedName("mo_ta") val description: String,
    @SerializedName("so_ky") val weight: Int = 0
) : Serializable

data class DichVuHanhLyResponse(
    @SerializedName("dich_vu_hanh_ly") val listDVHL: List<DichVuHanhLy>
) : Serializable

data class HanhLyPassenger(
    val hanhLy: DichVuHanhLy,
    val passengerTitles: String
)

