// src/main/java/com/example/datvemaybay/response/AddHHKResponse.kt

package com.example.datvemaybay.response

import com.google.gson.annotations.Expose
import com.google.gson.annotations.SerializedName

data class AddHHKResponse(
    @SerializedName("message")
    @Expose
    val message: String?,

    @SerializedName("status")
    @Expose
    val status: Boolean
)
