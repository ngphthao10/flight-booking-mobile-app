// src/main/java/com/example/datvemaybay/response/QuocGia.kt

package com.example.datvemaybay.response

import com.google.gson.annotations.Expose
import com.google.gson.annotations.SerializedName

data class QuocGiaResponse(
    @SerializedName("status")
    @Expose
    val status: Boolean,

    @SerializedName("data")
    @Expose
    val data: List<QuocGia>?
)

data class QuocGia(
    @SerializedName("MaQG")
    @Expose
    val maQG: String,

    @SerializedName("TenQG")
    @Expose
    val tenQG: String
)
