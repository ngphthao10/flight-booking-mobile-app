package com.example.datvemaybay.data.models

import java.io.Serializable

data class PassengerInfo(
    val title: String,
    val firstName: String,
    val lastName: String,
    val birthDate: String,
    val country: String,
    val idNumber: String
) : Serializable
