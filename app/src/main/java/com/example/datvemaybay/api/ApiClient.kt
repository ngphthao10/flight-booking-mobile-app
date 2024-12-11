// src/main/java/com/example/datvemaybay/api/ApiClient.kt

package com.example.datvemaybay.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ApiClient {
    private const val BASE_URL = "http://10.0.2.2:5000/" // Đối với Emulator
    // Nếu bạn đang sử dụng thiết bị thực, hãy thay bằng địa chỉ IP LAN của máy tính chủ, ví dụ:
    // private const val BASE_URL = "http://192.168.1.100:5000/"

    // Tạo Logging Interceptor
    private val logging = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    // Tạo OkHttpClient và thêm Interceptor
    private val client = OkHttpClient.Builder()
        .addInterceptor(logging)
        .build()

    // Tạo Retrofit instance
    val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(client) // Thêm OkHttpClient với Interceptor
        .addConverterFactory(GsonConverterFactory.create())
        .build()
}
