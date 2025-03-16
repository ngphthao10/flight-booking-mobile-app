package com.example.datvemaybay.data.models

import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class ContactPerson(
    @SerializedName("ho_nlh") val ho: String = "",
    @SerializedName("ten_nlh") val ten: String = "",
    @SerializedName("sdt") val phoneNumber: String = "",
    @SerializedName("email") val email: String = ""
) : Serializable

