package com.example.datvemaybay.ui.homepage

import android.annotation.SuppressLint
import android.app.Activity
import android.app.DatePickerDialog
import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.core.widget.addTextChangedListener
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.PassengerInfo
import com.example.datvemaybay.data.viewmodel.PassengerViewModel
import com.google.android.material.textfield.MaterialAutoCompleteTextView
import com.google.android.material.textfield.TextInputEditText
import java.util.Calendar

class PassengerInfoFragment : Fragment() {

    private lateinit var danhXungView: MaterialAutoCompleteTextView
    private lateinit var edtHo: TextInputEditText
    private lateinit var edtTen: TextInputEditText
    private lateinit var edtNgaySinh: TextInputEditText
    private lateinit var edtQuocGia: MaterialAutoCompleteTextView
    private lateinit var edtSoCCCD: TextInputEditText
    private lateinit var btnSave: Button
    private lateinit var viewModel: PassengerViewModel
    private lateinit var btnCanel: ImageButton
    private lateinit var btnReset: Button

    companion object {
        private const val ARG_PASSENGER_ID = "passenger_id"
        private  lateinit var passengerID : String

        fun newInstance(passengerId: String): PassengerInfoFragment {
            return PassengerInfoFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PASSENGER_ID, passengerId)
                    passengerID = passengerId
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewModel = ViewModelProvider(requireActivity())[PassengerViewModel::class.java]
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_passenger_info, container, false)
        initViews(view)
        setupDropdowns()
        setupListeners()
        loadPassengerData()
        return view
    }

    private fun initViews(view: View) {
        danhXungView = view.findViewById(R.id.danhXungView)
        edtHo = view.findViewById(R.id.edtHo)
        edtTen = view.findViewById(R.id.edtTen)
        edtNgaySinh = view.findViewById(R.id.edtNgaySinh)
        edtQuocGia = view.findViewById(R.id.countryAutoCompleteTextView)
        edtSoCCCD = view.findViewById(R.id.edtSoCCCD)
        btnSave = view.findViewById(R.id.btnSave)
        btnCanel = view.findViewById(R.id.btnCancel)
        btnReset = view.findViewById(R.id.btnReset)
    }

    private fun setupDropdowns() {
        val danhXungList = listOf("Ông", "Bà", "Cô")
        val danhXungAdapter = ArrayAdapter(requireContext(), androidx.appcompat.R.layout.support_simple_spinner_dropdown_item, danhXungList)
        danhXungView.setAdapter(danhXungAdapter)

        val countryList = listOf("Việt Nam", "Afghanistan", "Ả Rập Saudi", "Ai Cập", "Ấn Độ", "Argentina", "Ba Lan", "Bỉ", "Bồ Đào Nha", "Brazil")
        val countryAdapter = ArrayAdapter(requireContext(), androidx.appcompat.R.layout.support_simple_spinner_dropdown_item, countryList)
        edtQuocGia.setAdapter(countryAdapter)
    }

    private fun setupListeners() {
        danhXungView.setOnClickListener { danhXungView.showDropDown() }
        edtNgaySinh.setOnClickListener { showDatePickerDialog() }
        edtQuocGia.setOnClickListener { edtQuocGia.showDropDown() }

        edtHo.addTextChangedListener(createTextWatcher(edtHo, "Họ không được chứa số hoặc ký tự đặc biệt"))
        edtTen.addTextChangedListener(createTextWatcher(edtTen, "Tên không được chứa số hoặc ký tự đặc biệt"))
        edtSoCCCD.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                if (s != null && s.length != 12) {
                    edtSoCCCD.error = "Căn cước công dân phải có 12 chữ số"
                }
            }
        })

        btnSave.setOnClickListener { savePassengerData() }
        btnCanel.setOnClickListener {
            parentFragmentManager.popBackStack()
        }
        btnReset.setOnClickListener {
            danhXungView.text.clear()
            edtHo.text?.clear()
            edtTen.text?.clear()
            edtNgaySinh.text?.clear()
            edtQuocGia.text.clear()
            edtSoCCCD.text?.clear()
        }
    }

    private fun createTextWatcher(inputField: TextInputEditText, errorMessage: String): TextWatcher {
        return object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                if (s != null) {
                    // Kiểm tra nếu dữ liệu không hợp lệ
                    if (!s.toString().matches("^[a-zA-Z ]*$".toRegex())) {
                        inputField.error = errorMessage
                    } else {
                        inputField.error = null
                        Log.d("ValidData", "Dữ liệu hợp lệ: $s")
                    }
                }
                checkFormValidity()
            }
        }
    }

    private fun checkFormValidity() {
        // Kiểm tra xem có lỗi trong các trường không
        val isHoValid = edtHo.error == null
        val isTenValid = edtTen.error == null
        val isSoCCCDValid = edtSoCCCD.error == null

        Log.d("Click", "hehe ${edtHo.error} $isHoValid")
        Log.d("Click", "haha ${edtTen.error} $isTenValid")
        Log.d("Click", "hihi ${edtSoCCCD.error} $isSoCCCDValid")

        // Nếu tất cả đều hợp lệ thì kích hoạt nút "Save"
        btnSave.isClickable = isHoValid && isTenValid && isSoCCCDValid
        Log.d("Click", "Không thể bấm nút này ${btnSave.isClickable}")
    }

    @SuppressLint("SetTextI18n")
    private fun showDatePickerDialog() {
        val calendar = Calendar.getInstance()
        val passengerCategory = arguments?.getString(ARG_PASSENGER_ID) // Retrieve the passenger category

        // Default maximum and minimum dates
        var minAgeInMillis: Long = 0
        var maxAgeInMillis: Long = 0

        // Set date ranges based on passenger category
        if (passengerCategory != null) {
            when {
                passengerCategory.lowercase().contains("người lớn") -> {
                    // Người lớn (adults): age >= 12 years
                    maxAgeInMillis = System.currentTimeMillis() - (12L * 365 * 24 * 60 * 60 * 1000)
                }
                passengerCategory.lowercase().contains("trẻ em") -> {
                    // Trẻ em (children): age between 2-11 years
                    minAgeInMillis = System.currentTimeMillis() - (11L * 365 * 24 * 60 * 60 * 1000)
                    maxAgeInMillis = System.currentTimeMillis() - (2L * 365 * 24 * 60 * 60 * 1000)
                }
                passengerCategory.lowercase().contains("em bé") -> {
                    // Em bé (babies): age < 2 years
                    minAgeInMillis = System.currentTimeMillis() - (2L * 365 * 24 * 60 * 60 * 1000)
                }
            }
        }

        val datePickerDialog = DatePickerDialog(requireContext(), { _, year, month, dayOfMonth ->
            val selectedDate = Calendar.getInstance().apply {
                set(year, month, dayOfMonth)
            }

            val ageInMillis = System.currentTimeMillis() - selectedDate.timeInMillis
//            val isValidAge = when {
//                passengerCategory?.contains("người lớn") == true -> ageInMillis > 12L * 365 * 24 * 60 * 60 * 1000 // lớn hơn 12 tuổi
//                passengerCategory?.contains("trẻ em") == true -> ageInMillis in (2L * 365 * 24 * 60 * 60 * 1000)..(11L * 365 * 24 * 60 * 60 * 1000) // từ 2-11 tuổi
//                passengerCategory?.contains("em bé") == true -> ageInMillis < 2L * 365 * 24 * 60 * 60 * 1000 // nhỏ hơn 2 tuổi
//                else -> false
//            }

            edtNgaySinh.setText("$dayOfMonth-${month + 1}-$year")
        }, calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH))

        datePickerDialog.datePicker.maxDate = maxAgeInMillis
        datePickerDialog.datePicker.minDate = minAgeInMillis

        datePickerDialog.show()
    }


    private fun loadPassengerData() {
        arguments?.getString(ARG_PASSENGER_ID)?.let { passengerId ->
            viewModel.getPassengerData(passengerId)?.let { data ->
                danhXungView.setText(data.title, false)
                edtHo.setText(data.lastName)
                edtTen.setText(data.firstName)
                edtNgaySinh.setText(data.birthDate)
                edtQuocGia.setText(data.country, false)
                edtSoCCCD.setText(data.idNumber)
            }
        }
    }

    private fun savePassengerData() {
        if (edtHo.error != null || edtTen.error != null || edtSoCCCD.error != null || edtHo.text?.toString().isNullOrEmpty() || edtTen.text?.toString().isNullOrEmpty() || edtSoCCCD.text?.toString().isNullOrEmpty() || edtSoCCCD.text?.length != 12) {
            Toast.makeText(requireContext(), "Vui lòng nhập đầy đủ thông tin hợp lệ", Toast.LENGTH_SHORT).show()
            return
        }

        val passenger = PassengerInfo(
            title = danhXungView.text.toString().trim(),
            lastName = edtHo.text.toString().trim(),
            firstName = edtTen.text.toString().trim(),
            birthDate = edtNgaySinh.text.toString().trim(),
            country = edtQuocGia.text.toString().trim(),
            idNumber = edtSoCCCD.text.toString().trim()
        )

        arguments?.getString(ARG_PASSENGER_ID)?.let {
            viewModel.savePassengerData(passengerID, passenger)
            Toast.makeText(requireContext(), "Thông tin hành khách đã được lưu", Toast.LENGTH_SHORT).show()
            parentFragmentManager.popBackStack()
        }
    }

}
