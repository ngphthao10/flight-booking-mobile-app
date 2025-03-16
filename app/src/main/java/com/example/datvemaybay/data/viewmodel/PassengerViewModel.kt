package com.example.datvemaybay.data.viewmodel

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.datvemaybay.data.models.PassengerInfo

class PassengerViewModel : ViewModel() {
    val passengerData: MutableLiveData<Map<String, PassengerInfo>> = MutableLiveData()

    fun savePassengerData(id: String, passenger: PassengerInfo) {
        val currentData = passengerData.value ?: emptyMap()
        passengerData.value = currentData + (id to passenger)
    }

    fun getPassengerData(id: String): PassengerInfo? {
        return passengerData.value?.get(id)
    }
}
