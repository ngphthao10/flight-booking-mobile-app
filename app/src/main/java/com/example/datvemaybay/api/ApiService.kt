// src/main/java/com/example/datvemaybay/api/ApiService.kt

package com.example.datvemaybay.api

import com.example.datvemaybay.response.AddHHKResponse
import com.example.datvemaybay.response.HangHangKhongListResponse
import com.example.datvemaybay.response.QuocGiaResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    @GET("api/hang-hang-khong")
    fun getHangHangKhongList(): Call<HangHangKhongListResponse>

    @POST("api/hang-hang-khong")
    fun addHangHangKhong(@Body newHHK: HangHangKhongListResponse.DataItem): Call<AddHHKResponse>

    @GET("api/quoc-gia")
    fun getQuocGiaList(): Call<QuocGiaResponse>
}
