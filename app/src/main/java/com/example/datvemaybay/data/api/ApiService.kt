// src/main/java/com/example/datvemaybay/api/ApiService.kt

package com.example.datvemaybay.api

import com.example.datvemaybay.response.HangHangKhongData
import com.example.datvemaybay.response.QuocGiaResponse
import com.example.datvemaybay.response.UpdateHHKResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface ApiService {
    @GET("api/hang-hang-khong")
    fun getHangHangKhongList(): Call<HangHangKhongListResponse>

    @GET("api/hang-hang-khong/{maHHK}")
    fun getHangHangKhongDetail(@Path("maHHK") maHHK: String): Call<UpdateHHKResponse>

    @POST("api/hang-hang-khong")
    fun addHangHangKhong(@Body newHHK: HangHangKhongData): Call<AddHHKResponse>

    @PUT("api/hang-hang-khong/{maHHK}")
    fun updateHangHangKhong(@Path("maHHK") maHHK: String, @Body currentHHK: HangHangKhongData):
            Call<UpdateHHKResponse>

    @DELETE("api/hang-hang-khong/{maHHK}")
    fun deleteHangHangKhong(@Path("maHHK") maHHK: String): Call<AddHHKResponse>

    @GET("api/quoc-gia")
    fun getQuocGiaList(): Call<QuocGiaResponse>
}
