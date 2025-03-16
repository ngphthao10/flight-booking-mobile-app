package com.example.datvemaybay.data.viewmodel

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.datvemaybay.data.models.ContactPerson

class ContactPersonViewModel : ViewModel() {
    val contactPersonData = MutableLiveData<ContactPerson>()
}