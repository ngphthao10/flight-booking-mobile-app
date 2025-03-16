// src/main/java/com/example/datvemaybay/api/ApiService.kt

package com.example.datvemaybay.data.api

import BookingResponse
import FlightBooking
import com.example.datvemaybay.data.models.ChuyenBayRequest
import com.example.datvemaybay.data.models.ChuyenBayResponse
import com.example.datvemaybay.data.models.ChuyenBayServiceResponse
import com.example.datvemaybay.data.models.DichVuHanhLyResponse
import com.example.datvemaybay.data.models.KhuyenMaiRequest
import com.example.datvemaybay.data.models.KhuyenMaiResponse
import com.example.datvemaybay.data.models.LoaiGheRequest
import com.example.datvemaybay.data.models.PaymentData
import com.example.datvemaybay.data.models.SanBayResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface ApiService {
//    @GET("api/hang-hang-khong")
//    fun getHangHangKhongList(): Call<HangHangKhongListResponse>
//
//    @GET("api/hang-hang-khong/{maHHK}")
//    fun getHangHangKhongDetail(@Path("maHHK") maHHK: String): Call<UpdateHHKResponse>
//
//    @POST("api/hang-hang-khong")
//    fun addHangHangKhong(@Body newHHK: HangHangKhongData): Call<AddHHKResponse>
//
//    @PUT("api/hang-hang-khong/{maHHK}")
//    fun updateHangHangKhong(@Path("maHHK") maHHK: String, @Body currentHHK: HangHangKhongData):
//            Call<UpdateHHKResponse>
//
//    @DELETE("api/hang-hang-khong/{maHHK}")
//    fun deleteHangHangKhong(@Path("maHHK") maHHK: String): Call<AddHHKResponse>
//
    @GET("api/all-san-bay")
    fun getSanBayList(): Call<SanBayResponse>

    @POST("api/flights/search")
    fun getChuyenBay(@Body request: ChuyenBayRequest): Call<ChuyenBayResponse>

    @POST("api/flights/{maChuyenBay}/services")
    fun getChuyenBayService(
        @Path("maChuyenBay") maChuyenBay: String,
        @Body loaiGhe: LoaiGheRequest
    ): Call<ChuyenBayServiceResponse>

    @GET("api/flights/{ma_chuyen_bay}/luggage-services")
    fun getDichVuHanhLyChuyenBay(
        @Path("ma_chuyen_bay") flightID: String
    ): Call<DichVuHanhLyResponse>

    @POST("/api/booking")
    fun setBookingData(
        @Body flightBooking: FlightBooking
    ): Call<BookingResponse>

    @POST("/api/bookings/promotions")
    fun getKhuyenMaiPromotions(
        @Body khuyenMaiRequest: KhuyenMaiRequest
    ): Call<KhuyenMaiResponse>

    @POST("/api/bookings/{booking_id}/{user_id}/confirm")
    fun getThanhToanResponse(
        @Path("booking_id") bookingID: String,
        @Path("user_id") userID: Int,
        @Body paymentData: PaymentData
    ): Call<Any>
}
