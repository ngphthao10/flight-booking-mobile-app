package com.example.datvemaybay.ui.homepage

import android.os.Bundle
import android.text.Editable
import android.text.InputFilter
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.datvemaybay.R
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import com.google.android.material.textfield.TextInputEditText

class NganHangFragment : BottomSheetDialogFragment() {

    private lateinit var edtSoThe: TextInputEditText
    private lateinit var edtHoTen: TextInputEditText
    private lateinit var radioGroup: RadioGroup

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_ngan_hang, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Khởi tạo view
        edtSoThe = view.findViewById(R.id.edtSoThe)
        edtHoTen = view.findViewById(R.id.edtHoTen)
        radioGroup = view.findViewById(R.id.radioGroup)

        // Chỉ cho phép nhập số vào ô số thẻ
        edtSoThe.filters = arrayOf<InputFilter>(InputFilter.LengthFilter(16)) // Giới hạn số ký tự là 16

        // Chỉ cho phép nhập chữ và khoảng trắng vào ô họ tên
        edtHoTen.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}

            override fun afterTextChanged(s: Editable?) {
                s?.let {
                    val filtered = it.toString().replace("[^a-zA-Z\\s]".toRegex(), "")
                    if (filtered != it.toString()) {
                        edtHoTen.setText(filtered)
                        edtHoTen.setSelection(filtered.length)
                    }
                }
            }
        })

        val confirmButton: Button = view.findViewById(R.id.confirmButton)
        confirmButton.setOnClickListener {
            val soThe = edtSoThe.text.toString()
            val hoTen = edtHoTen.text.toString()
            val selectedRadioButtonId = radioGroup.checkedRadioButtonId

            if (soThe.isEmpty() || hoTen.isEmpty() || selectedRadioButtonId == -1) {
                Toast.makeText(context, "Vui lòng điền đầy đủ thông tin", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val selectedBank = view.findViewById<RadioButton>(selectedRadioButtonId).text.toString()

            // Truyền dữ liệu về Activity
            val activity = activity as? OnDataPass
            activity?.onDataPass(soThe, hoTen, selectedBank)

            dismiss() // Đóng BottomSheet
        }
        val btnCancel: ImageButton = view.findViewById(R.id.btnCancel)
        btnCancel.setOnClickListener { dismiss() }
    }

    interface OnDataPass {
        fun onDataPass(soThe: String, hoTen: String, nganHang: String)
    }
}

