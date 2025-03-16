package com.example.datvemaybay.data.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.datvemaybay.data.models.DichVuHanhLy
import com.example.datvemaybay.data.models.HanhLyPassenger

class LuggageViewModel : ViewModel() {

    private val _selectedLuggageData = MutableLiveData<MutableMap<Int, MutableList<HanhLyPassenger>>>()
    val selectedLuggageData: LiveData<MutableMap<Int, MutableList<HanhLyPassenger>>> get() = _selectedLuggageData

    fun setSelectedLuggageData(data: MutableMap<Int, MutableList<HanhLyPassenger>>) {
        _selectedLuggageData.value = data
    }
}