package com.example.datvemaybay.ui.homepage

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.RadioButton
import com.example.datvemaybay.R
import com.google.android.material.bottomsheet.BottomSheetDialogFragment

class ClassFragment : BottomSheetDialogFragment() {

    private var selectedSeatClass: String? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_class, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Lấy các RadioButton
        val rbEconomy = view.findViewById<RadioButton>(R.id.rbEconomy)
        val rbBusiness = view.findViewById<RadioButton>(R.id.rbBusiness)

        // Nhận dữ liệu đã chọn trước đó (nếu có)
        selectedSeatClass = arguments?.getString("class_result")

        // Thiết lập trạng thái ban đầu của RadioButton
        when (selectedSeatClass) {
            "Economy" -> rbEconomy.isChecked = true
            "Business" -> rbBusiness.isChecked = true
        }

        // Lắng nghe sự kiện chọn
        val listener = View.OnClickListener { button ->
            selectedSeatClass = when (button.id) {
                R.id.rbEconomy -> "Economy"
                R.id.rbBusiness -> "Business"
                else -> ""
            }

            // Truyền dữ liệu về MainActivity
            val result = Bundle().apply {
                putString("class_result", selectedSeatClass)
            }
            parentFragmentManager.setFragmentResult("class_result", result)

            // Đóng BottomSheetDialogFragment
            dismiss()
        }

        rbEconomy.setOnClickListener(listener)
        rbBusiness.setOnClickListener(listener)
    }

    companion object {
        fun newInstance(selectedSeatClass: String?): ClassFragment {
            val fragment = ClassFragment()
            val args = Bundle().apply {
                putString("class_result", selectedSeatClass)
            }
            fragment.arguments = args
            return fragment
        }
    }

}