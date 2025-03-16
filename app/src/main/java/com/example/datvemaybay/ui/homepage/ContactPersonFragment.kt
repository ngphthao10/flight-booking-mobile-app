package com.example.datvemaybay.ui.homepage

import android.content.Context
import android.os.Bundle
import android.util.Patterns
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import androidx.lifecycle.ViewModelProvider
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.ContactPerson
import com.example.datvemaybay.data.viewmodel.ContactPersonViewModel
import com.google.android.material.textfield.TextInputEditText


class ContactPersonFragment : Fragment() {

    private lateinit var edtHo: TextInputEditText
    private lateinit var edtTen: TextInputEditText
    private lateinit var edtSDT: TextInputEditText
    private lateinit var edtEmail: TextInputEditText
    private lateinit var btnSave: Button
    private lateinit var btnCancel: ImageButton
    private lateinit var btnReset: Button
    private lateinit var maDienThoai: TextInputEditText

    private lateinit var viewModel: ContactPersonViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_contact_person, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        edtHo = view.findViewById(R.id.edtHo)
        edtTen = view.findViewById(R.id.edtTen)
        edtSDT = view.findViewById(R.id.edtSDT)
        edtEmail = view.findViewById(R.id.edtEmail)
        btnSave = view.findViewById(R.id.btnSave)
        btnCancel = view.findViewById(R.id.btnCancel)
        btnReset = view.findViewById(R.id.btnReset)
        maDienThoai = view.findViewById(R.id.maDienThoai)
        maDienThoai.isFocusable = false
        maDienThoai.isClickable = false

        viewModel = ViewModelProvider(requireActivity())[ContactPersonViewModel::class.java]

        // Restore data if available
        viewModel.contactPersonData.value?.let { contactPerson ->
            edtHo.setText(contactPerson.ho)
            edtTen.setText(contactPerson.ten)
            edtSDT.setText(contactPerson.phoneNumber)
            edtEmail.setText(contactPerson.email)
        }

        btnSave.setOnClickListener {
            if (validateInputs()) {
                val contactPerson = ContactPerson(
                    ho = edtHo.text.toString(),
                    ten = edtTen.text.toString(),
                    phoneNumber = edtSDT.text.toString(),
                    email = edtEmail.text.toString()
                )
                viewModel.contactPersonData.value = contactPerson
                parentFragmentManager.popBackStack()
            }
        }

        btnCancel.setOnClickListener {
            parentFragmentManager.popBackStack()
        }

        btnReset.setOnClickListener {
            edtHo.text?.clear()
            edtTen.text?.clear()
            edtSDT.text?.clear()
            edtEmail.text?.clear()
        }
    }

    private fun validateInputs(): Boolean {
        var isValid = true

        if (edtHo.text.isNullOrBlank() || !edtHo.text.toString().matches(Regex("^[a-zA-Z]+$"))) {
            edtHo.error = "Chỉ được nhập chữ cái"
            isValid = false
        }

        if (edtTen.text.isNullOrBlank() || !edtTen.text.toString().matches(Regex("^[a-zA-Z\\s]+$"))) {
            edtTen.error = "Chỉ được nhập chữ cái và khoảng trống"
            isValid = false
        }

        if (edtSDT.text.isNullOrBlank() || !edtSDT.text.toString().matches(Regex("^\\d{9}$"))) {
            edtSDT.error = "Số điện thoại phải là 9 chữ số"
            isValid = false
        }

        if (edtEmail.text.isNullOrBlank() || !Patterns.EMAIL_ADDRESS.matcher(edtEmail.text.toString()).matches()) {
            edtEmail.error = "Địa chỉ email không hợp lệ"
            isValid = false
        }

        return isValid
    }
}
